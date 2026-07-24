"""
Reports/users_report.py — ATAMS Users Reports module.

Report 1: User Information.

Data source: BioStar 2 local server API via biostar_connector.

VERIFIED BEHAVIOURS (tested against the live server, do not change on assumption)
--------------------------------------------------------------------------------
1. /api/users?group_id=X is RECURSIVE. It returns the group's own direct members
   plus every member of every descendant group. Confirmed twice:
     - group 1004 (CORPORATE): 0 direct members, returns 68 = sum of 9 children
     - group 1022 (Aviation Security): 427 direct + 18 in child = returns 445
   Therefore we never expand a subtree before fetching. One group_id per query.

2. Each user belongs to EXACTLY ONE group. Confirmed by arithmetic:
     group 1    (All Users)         -> 1919  (whole system)
     group 5760 (Active Staff)      -> 1326
     group 1016 (NONE Active STAFFS)->  352
     241 + 1326 + 352 = 1919, where 241 sit directly on the All Users root.
   Those 241 have no directorate and no department. They are flagged, not hidden.

3. limit / offset pagination works (limit=10 on a 445-user group returned 10).

4. EVERY value in the payload is a STRING, including booleans and counts.
   "false" is truthy in Python. All coercion happens in _coerce_user() and
   nowhere else. Never test a raw payload value for truthiness.

5. The `department` field on a user record is free text, frequently absent, and
   sometimes CONTRADICTS the group tree (user 812 is in group "Information
   Technology" but carries department "Corporate"). It is deliberately ignored.
   Department and directorate are derived from the group tree instead.

6. Datetimes are UTC with a two-digit fraction ("2030-12-31T23:00:00.00Z").
   Uganda is fixed UTC+3 with no DST. Converted to EAT for display.
"""

from datetime import datetime, timedelta, timezone

from biostar_connector import get_user_groups, get_users_in_group

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

PAGE_SIZE = 100
MAX_PAGES = 100  # safety cap: 10,000 users. Guards against a bad total.

EAT = timezone(timedelta(hours=3))  # Uganda, fixed, no DST

ROOT_GROUP_ID = "1"          # All Users
ACTIVE_STAFF_ID = "5760"     # Active Staff
NONE_ACTIVE_ID = "1016"      # NONE Active STAFFS

# Groups whose direct children are the directorates.
TOP_LEVEL_IDS = {ACTIVE_STAFF_ID, NONE_ACTIVE_ID}

# The custom field that holds staff grade. Confirmed on this server:
#   id 2 = Mileage, id 4 = Category, id 5 = Weekly_Fuel
CATEGORY_CUSTOM_FIELD_ID = "4"

_group_index_cache = None


# --------------------------------------------------------------------------
# Coercion helpers — the only place raw strings become Python types
# --------------------------------------------------------------------------

def _as_str(value, default=""):
    """Keep IDs as strings. Never int() a user_id: '02954' would become 2954."""
    if value is None:
        return default
    return str(value).strip()


def _as_bool(value, default=False):
    """BioStar sends 'true'/'false' as strings. Both are truthy in Python."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def _as_int(value, default=0):
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _parse_biostar_utc(value):
    """
    Parse '2030-12-31T23:00:00.00Z' -> aware UTC datetime, or None.

    The two-digit fraction is not universally accepted by fromisoformat across
    Python versions, so the fraction is normalised to 6 digits first.
    """
    text = _as_str(value)
    if not text:
        return None

    text = text.rstrip("Z")
    if "." in text:
        base, frac = text.split(".", 1)
        frac = (frac + "000000")[:6]
        text = f"{base}.{frac}"
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
    else:
        fmt = "%Y-%m-%dT%H:%M:%S"

    try:
        return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _utc_to_eat_string(value):
    """UTC string -> 'YYYY-MM-DD HH:MM' in EAT. Empty string if unparseable."""
    parsed = _parse_biostar_utc(value)
    if parsed is None:
        return ""
    return parsed.astimezone(EAT).strftime("%Y-%m-%d %H:%M")


# --------------------------------------------------------------------------
# Group tree
# --------------------------------------------------------------------------

def build_group_index(raw_response):
    """
    Flatten the /api/user_groups response into {group_id: {...}}.

    parent_id arrives as an OBJECT ({"id": "1006", "name": "DSSER"}), not a
    scalar. It is unwrapped to a plain string id here.
    """
    rows = (raw_response or {}).get("UserGroupCollection", {}).get("rows", [])
    index = {}

    for row in rows:
        group_id = _as_str(row.get("id"))
        if not group_id:
            continue

        parent = row.get("parent_id")
        parent_id = _as_str(parent.get("id")) if isinstance(parent, dict) else ""

        index[group_id] = {
            "id": group_id,
            "name": _as_str(row.get("name")),
            "parent_id": parent_id,
            "depth": _as_int(row.get("depth")),
            "user_count": _as_int(row.get("user_count")),
        }

    return index


def get_group_index(force_refresh=False):
    """Cached group index. The tree changes rarely; refresh explicitly."""
    global _group_index_cache
    if _group_index_cache is None or force_refresh:
        _group_index_cache = build_group_index(get_user_groups())
    return _group_index_cache


def get_descendants(index, group_id):
    """
    All descendant group ids of group_id, including group_id itself.

    NOT needed for fetching (the API recurses). Used for rendering the picker
    and for any local counting.
    """
    target = _as_str(group_id)
    if target not in index:
        return set()

    children = {}
    for gid, group in index.items():
        children.setdefault(group["parent_id"], []).append(gid)

    found, stack = set(), [target]
    while stack:
        current = stack.pop()
        if current in found:
            continue  # defensive: a cycle would otherwise hang this loop
        found.add(current)
        stack.extend(children.get(current, []))

    return found


def resolve_directorate(index, group_id):
    """
    Walk up the tree to the directorate — the node whose parent is Active Staff
    or NONE Active STAFFS.

    Transport (1065) -> Administration -> HUMAN RESOURCE & ADMIN
    Revenue Collection Assistants (1072) -> Revenue -> Finance -> FINANCE

    Returns "" for the root and for the two top-level container groups, since
    neither is a directorate.
    """
    current = _as_str(group_id)
    if current in TOP_LEVEL_IDS or current == ROOT_GROUP_ID or current not in index:
        return ""

    seen = set()
    while current in index and current not in seen:
        seen.add(current)
        parent = index[current]["parent_id"]
        if parent in TOP_LEVEL_IDS:
            return index[current]["name"]
        if not parent or parent == ROOT_GROUP_ID:
            return ""
        current = parent

    return ""


# --------------------------------------------------------------------------
# Field extraction
# --------------------------------------------------------------------------

def _extract_category(record):
    """
    Pull staff grade out of user_custom_fields.

    Values carry a LEADING SPACE on this server (" Principal", " Manager"), and
    the 'item' key is simply absent when the value is empty. Both handled.
    """
    for field in record.get("user_custom_fields") or []:
        definition = field.get("custom_field") or {}
        if _as_str(definition.get("id")) == CATEGORY_CUSTOM_FIELD_ID:
            return _as_str(field.get("item"))
    return ""


def _summarise_credentials(record):
    """Human-readable credential list, plus a flag for having none at all."""
    parts = []
    counts = [
        ("Fingerprint", _as_int(record.get("fingerprint_template_count"))),
        ("Face", _as_int(record.get("face_count"))),
        ("Visual Face", _as_int(record.get("visual_face_count"))),
        ("Card", _as_int(record.get("card_count"))),
        ("QR", _as_int(record.get("qr_count"))),
        ("Mobile", _as_int(record.get("mobile_count"))),
    ]
    for label, count in counts:
        if count > 0:
            parts.append(f"{label} ({count})" if count > 1 else label)

    if _as_bool(record.get("pin_exists")):
        parts.append("PIN")

    total = sum(count for _, count in counts)
    has_pin = _as_bool(record.get("pin_exists"))

    return {
        "credentials": ", ".join(parts) if parts else "None",
        "has_no_credentials": total == 0 and not has_pin,
    }


def _extract_status(record):
    """Combine the disabled / expired flags into one readable status."""
    disabled = _as_bool(record.get("disabled"))
    expired = _as_bool(record.get("expired"))
    if disabled and expired:
        return "Disabled, Expired"
    if disabled:
        return "Disabled"
    if expired:
        return "Expired"
    return "Active"


def _coerce_user(record, index):
    """Turn one fat raw user record into one flat display row."""
    group = record.get("user_group_id") or {}
    group_id = _as_str(group.get("id"))
    group_name = _as_str(group.get("name"))

    permission = record.get("permission") or {}
    credentials = _summarise_credentials(record)

    unassigned = group_id == ROOT_GROUP_ID or not group_id

    return {
        "user_id": _as_str(record.get("user_id")),
        "name": _as_str(record.get("name")),
        "department": "" if unassigned else group_name,
        "directorate": resolve_directorate(index, group_id),
        "category": _extract_category(record),
        "credentials": credentials["credentials"],
        "has_no_credentials": credentials["has_no_credentials"],
        "operator_role": _as_str(permission.get("name")),
        "login_id": _as_str(record.get("login_id")),
        "status": _extract_status(record),
        "disabled": _as_bool(record.get("disabled")),
        "expired": _as_bool(record.get("expired")),
        "start_date": _utc_to_eat_string(record.get("start_datetime")),
        "expiry_date": _utc_to_eat_string(record.get("expiry_datetime")),
        "group_id": group_id,
        "unassigned": unassigned,
    }


# --------------------------------------------------------------------------
# Report 1 — User Information
# --------------------------------------------------------------------------

def fetch_all_users_in_group(group_id):
    """
    Page through every user in a group subtree.

    The API is recursive, so one group_id covers the whole branch. The loop is
    capped by MAX_PAGES so a wrong 'total' cannot spin forever.
    """
    collected, offset, total, pages = [], 0, None, 0

    while pages < MAX_PAGES:
        payload = get_users_in_group(group_id, limit=PAGE_SIZE, offset=offset)
        collection = payload.get("UserCollection") or {}
        rows = collection.get("rows") or []

        if total is None:
            total = _as_int(collection.get("total"))

        if not rows:
            break

        collected.extend(rows)
        offset += len(rows)
        pages += 1

        if total is not None and len(collected) >= total:
            break

    return collected, (total or len(collected))


def get_user_information(group_id=ACTIVE_STAFF_ID):
    """
    Report 1 — User Information.

    One row per user in the selected group subtree. Defaults to Active Staff
    (1326 users) rather than All Users (1919), so exited staff are included only
    when deliberately selected.

    Returns a dict carrying the rows plus enough metadata for the frontend to
    show what was actually fetched.
    """
    index = get_group_index()
    selected = _as_str(group_id)

    raw_users, total = fetch_all_users_in_group(selected)
    rows = [_coerce_user(record, index) for record in raw_users]

    group = index.get(selected, {})
    unassigned_count = sum(1 for row in rows if row["unassigned"])

    return {
        "group": {
            "id": selected,
            "name": group.get("name", "Unknown group"),
            "directorate": resolve_directorate(index, selected),
        },
        "reported_total": total,
        "returned": len(rows),
        "complete": len(rows) >= total,
        "unassigned_count": unassigned_count,
        "rows": rows,
    }


def list_group_tree():
    """
    Flat, ordered list of groups for the frontend picker.

    Each entry carries its depth so the UI can indent it without rebuilding the
    tree in JavaScript.
    """
    index = get_group_index()
    children = {}
    for gid, group in index.items():
        children.setdefault(group["parent_id"], []).append(gid)

    for siblings in children.values():
        siblings.sort(key=lambda gid: index[gid]["name"].strip().lower())

    ordered = []

    def walk(parent_id, depth):
        for gid in children.get(parent_id, []):
            group = index[gid]
            ordered.append({
                "id": gid,
                "name": group["name"].strip(),
                "depth": depth,
                "direct_user_count": group["user_count"],
                "is_directorate": group["parent_id"] in TOP_LEVEL_IDS,
            })
            walk(gid, depth + 1)

    walk("", 0)  # groups with no parent — the All Users root
    return ordered
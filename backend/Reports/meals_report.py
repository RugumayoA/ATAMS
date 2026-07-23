"""
Reports/meals.py
Meal punch reports, sourced from the BioStar local events API.

One report per meal device. Each report covers a single EAT calendar day.

Data source: POST /api/events/search on the local BioStar server
(via biostar_connector.search_events). This is the raw device event
stream - one row per punch - NOT the WSO2 daily attendance summary.

Reports:
    1. daily_meal_punches    - every punch on a device (one row per punch)
    2. staff_who_punched     - distinct staff on a device (one row per person)
    3. meal_punches_by_device - totals across all meal devices
"""

from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone

from biostar_connector import search_events


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Uganda is a fixed UTC+3 with no daylight saving, so this offset is exact.
EAT = timezone(timedelta(hours=3))

# The five meal devices, confirmed from the DeviceCollection payload.
# Sourced by ID rather than name-matching so a device rename can't
# silently drop one from the reports.
MEAL_DEVICES = {
    "939276804": "Meal Evanges-2",
    "939344349": "Meals_FZS AIRPORT",
    "939754293": "Meals-FZS CARGO",
    "939754211": "MEALS TEST",
    "939344350": "Meals_HQ HOUSE7",
}


# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------

def eat_day_to_utc_window(day: date) -> tuple[str, str]:
    """
    Convert a local EAT calendar day into the UTC window used by the
    events/search `datetime` filter (operator 3 = BETWEEN).

    The API filters on `datetime`, which is UTC. A local EAT day therefore
    maps to a window shifted back three hours.

    eat_day_to_utc_window(date(2026, 7, 21))
        -> ("2026-07-20T21:00:00Z", "2026-07-21T20:59:59Z")
    """
    start_eat = datetime(day.year, day.month, day.day, 0, 0, 0, tzinfo=EAT)
    end_eat = datetime(day.year, day.month, day.day, 23, 59, 59, tzinfo=EAT)

    def fmt(dt):
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return fmt(start_eat), fmt(end_eat)


def record_to_eat(record: dict) -> datetime:
    """
    Convert an event's UTC `datetime` into an EAT-aware datetime.

    Use this for BOTH display and day-bucketing. Never slice the raw UTC
    string for a date: a late supper punch near midnight would land on the
    wrong day.
    """
    raw = record["datetime"].replace("Z", "").split(".")[0]
    utc = datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    return utc.astimezone(EAT)


# ---------------------------------------------------------------------------
# Report 1: Daily Meal Punches (per device)
# ---------------------------------------------------------------------------

def daily_meal_punches(device_id: str, day: date) -> dict:
    """
    Every meal punch recorded on ONE device for ONE EAT calendar day.

    One output row per punch. A person who punched twice appears twice -
    this is the raw event stream, not a per-user daily summary.

    No filtering by event code. Every code that the device emitted is
    carried through on each row so the consumer can split accepted /
    denied / other downstream without re-querying the API.

    Returns:
        {
            "device_id":   str,
            "device_name": str,
            "date":        "YYYY-MM-DD",   (EAT)
            "total":       int,
            "rows":        [ {...}, ... ]  (chronological)
        }
    """
    start, end = eat_day_to_utc_window(day)

    body = {
        "Query": {
            "limit": 9999,
            "conditions": [
                {"column": "datetime", "operator": 3, "values": [start, end]},
                {"column": "device_id", "operator": 2, "values": [device_id]},
                # operator 1 on the group column: confirmed empirically to
                # exclude device/system events (which carry no user), leaving
                # only rows attributable to a person.
                {"column": "user_group_id.id", "operator": 1, "values": ["0"]},
            ],
            "orders": [{"column": "datetime", "descending": False}],
        }
    }

    raw_rows = search_events(body)["EventCollection"]["rows"]

    rows = []
    device_name = MEAL_DEVICES.get(device_id, device_id)

    for r in raw_rows:
        user = r.get("user_id", {})
        if not user.get("user_id"):
            # Defensive: a system event with no person attached. The group
            # condition should already have removed these.
            continue

        punch_eat = record_to_eat(r)
        device = r.get("device_id", {})

        rows.append({
            "date": punch_eat.strftime("%Y-%m-%d"),
            "time": punch_eat.strftime("%H:%M:%S"),
            "userId": user.get("user_id"),
            "userName": (user.get("name") or "").strip(),
            "userGroupName": r.get("user_group_id", {}).get("name", ""),
            "deviceId": device.get("id", device_id),
            "deviceName": device.get("name", device_name),
            "eventCode": r.get("event_type_id", {}).get("code", ""),
        })

    return {
        "device_id": device_id,
        "device_name": device_name,
        "date": day.strftime("%Y-%m-%d"),
        "total": len(rows),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Report 2: Staff who punched at a device
# ---------------------------------------------------------------------------

def staff_who_punched(device_id: str, day: date) -> dict:
    """
    Distinct staff who punched at ONE device on ONE EAT calendar day.

    This is the "staff meal report per device" deliverable: one row per
    PERSON rather than per punch. Someone who punched twice appears once,
    with punchCount = 2 and both times listed.

    Reuses daily_meal_punches, so this costs the same single API call.

    Returns:
        {
            "device_id":    str,
            "device_name":  str,
            "date":         "YYYY-MM-DD",   (EAT)
            "staffCount":   int,   distinct people
            "totalPunches": int,   punch events (>= staffCount)
            "staff":        [ {...}, ... ]  (first punch order)
        }
    """
    report = daily_meal_punches(device_id, day)

    staff = OrderedDict()
    for row in report["rows"]:
        uid = row["userId"]
        if uid not in staff:
            staff[uid] = {
                "userId": uid,
                "userName": row["userName"],
                "userGroupName": row["userGroupName"],
                "punchCount": 0,
                "firstPunch": row["time"],
                "times": [],
                "eventCodes": [],
            }
        staff[uid]["punchCount"] += 1
        staff[uid]["times"].append(row["time"])
        staff[uid]["eventCodes"].append(row["eventCode"])

    return {
        "device_id": report["device_id"],
        "device_name": report["device_name"],
        "date": report["date"],
        "staffCount": len(staff),
        "totalPunches": report["total"],
        "staff": list(staff.values()),
    }


# ---------------------------------------------------------------------------
# Report 3: Per-device summary
# ---------------------------------------------------------------------------

def meal_punches_by_device(day: date, device_ids: list[str] | None = None) -> dict:
    """
    Totals for each meal device on one EAT calendar day.

    One API call per device, matching the "each device has its own report"
    model. Reports both distinct staff and total punches per device.

    Returns:
        {
            "date":         "YYYY-MM-DD",
            "totalPunches": int,   all devices combined
            "devices":      [ {device_id, device_name, staffCount, totalPunches}, ... ]
        }
    """
    if device_ids is None:
        device_ids = list(MEAL_DEVICES.keys())

    devices = []
    grand_total = 0

    for device_id in device_ids:
        report = staff_who_punched(device_id, day)
        devices.append({
            "device_id": report["device_id"],
            "device_name": report["device_name"],
            "staffCount": report["staffCount"],
            "totalPunches": report["totalPunches"],
        })
        grand_total += report["totalPunches"]

    devices.sort(key=lambda d: d["totalPunches"], reverse=True)

    return {
        "date": day.strftime("%Y-%m-%d"),
        "totalPunches": grand_total,
        "devices": devices,
    }


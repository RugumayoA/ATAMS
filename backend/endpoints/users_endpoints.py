"""
endpoints/user_endpoints.py — ATAMS Users Reports API.

Blueprint: users_bp, registered in app.py at prefix /api/users

Routes
------
GET /api/users/groups
    The full group tree, flat and pre-ordered with depth, for the frontend
    picker. Call this once on page load.

GET /api/users/information?group_id=5760
    Report 1 — User Information. One row per user in the selected group
    subtree. Defaults to Active Staff (1326 users) rather than All Users
    (1919), so exited staff appear only when deliberately selected.

Notes for the Systems Admin
---------------------------
- The BioStar server is on the CAA LAN (192.168.0.230). Off-network requests
  fail with a connection timeout, which is returned here as HTTP 503 with a
  plain-English message rather than a Flask stack trace.
- Aviation Security (445 users) takes roughly five round trips to page. Larger
  selections take proportionally longer; All Users is 1919 users.
"""

from flask import Blueprint, jsonify, request
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, Timeout

from Reports.user_reports import (
    ACTIVE_STAFF_ID,
    get_group_index,
    get_user_information,
    list_group_tree,
)

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


def _unreachable_response(exc):
    """The single most likely failure in this module: not on the CAA network."""
    return jsonify({
        "error": "biostar_unreachable",
        "message": (
            "Could not reach the BioStar server. Check that you are on the CAA "
            "network or connected to the VPN."
        ),
        "detail": str(exc),
    }), 503


@users_bp.route("/groups", methods=["GET"])
def groups():
    """Group tree for the picker. Cached server-side after the first call."""
    try:
        tree = list_group_tree()
    except (RequestsConnectionError, Timeout) as exc:
        return _unreachable_response(exc)
    except HTTPError as exc:
        return jsonify({
            "error": "biostar_error",
            "message": "The BioStar server rejected the group request.",
            "detail": str(exc),
        }), 502

    return jsonify({"count": len(tree), "groups": tree}), 200


@users_bp.route("/information", methods=["GET"])
def information():
    """Report 1 — User Information."""
    group_id = (request.args.get("group_id") or ACTIVE_STAFF_ID).strip()

    if not group_id.isdigit():
        return jsonify({
            "error": "invalid_group_id",
            "message": "group_id must be numeric.",
        }), 400

    try:
        # Reject unknown ids up front. Without this the API returns an empty
        # collection and the page renders a blank table that looks like a bug.
        index = get_group_index()
        if group_id not in index:
            return jsonify({
                "error": "unknown_group_id",
                "message": f"No group with id {group_id} exists on this server.",
            }), 404

        report = get_user_information(group_id)

    except (RequestsConnectionError, Timeout) as exc:
        return _unreachable_response(exc)
    except HTTPError as exc:
        return jsonify({
            "error": "biostar_error",
            "message": "The BioStar server rejected the user request.",
            "detail": str(exc),
        }), 502

    return jsonify(report), 200
from flask import Blueprint, jsonify

from Reports.leave_reports import get_staff_on_leave, get_leave_reconciliation


leave_bp = Blueprint("leave", __name__, url_prefix="/api/leave")


@leave_bp.route("/staff-on-leave", methods=["GET"])
def staff_on_leave():
    return jsonify(get_staff_on_leave())


@leave_bp.route("/reconciliation", methods=["GET"])
def leave_reconciliation():
    return jsonify(get_leave_reconciliation())

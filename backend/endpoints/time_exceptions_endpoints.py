from flask import Blueprint, jsonify, request

from Reports.time_exception_reports import time_exception_by_tab


time_exceptions_bp = Blueprint("time_exceptions", __name__, url_prefix="/api/time_exceptions")


@time_exceptions_bp.route("/<tab>", methods=["POST"])
def get_time_exceptions(tab):
    """
    POST /api/time_exceptions/<tab>

    <tab> must be one of:
        late_clock_in, early_clock_out, early_clock_in, late_clock_out,
        incomplete_attendance, abscondment, low_working_hours,
        meal_punch_only   (placeholder - always returns empty)

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-01",
        "user_ids":   ["1141", "1142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    try:
        result = time_exception_by_tab(tab, start_date, end_date, user_ids)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(result)
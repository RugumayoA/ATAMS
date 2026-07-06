from flask import Blueprint, jsonify, request

from Reports.time_exception_reports import late_clock_in_report, early_clock_out_report, early_clock_in_report, late_clock_out_report, incomplete_attendance_report, abscondment_report, meal_punch_only_report


time_exceptions_bp = Blueprint("time_exceptions", __name__, url_prefix="/api/time_exceptions")


@time_exceptions_bp.route("/late_clock_in", methods=["POST"])
def get_late_clock_in():
    """
    POST /api/time_exceptions/late_clock_in

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-01",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = late_clock_in_report(start_date, end_date, user_ids)
    return jsonify(result)







@time_exceptions_bp.route("/early_clock_out", methods=["POST"])
def get_early_clock_out():
    """
    POST /api/time_exceptions/early_clock_out

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-07",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = early_clock_out_report(start_date, end_date, user_ids)
    return jsonify(result)


from Reports.time_exception_reports import (
    late_clock_in_report,
    early_clock_out_report,
    early_clock_in_report,
)


@time_exceptions_bp.route("/early_clock_in", methods=["POST"])
def get_early_clock_in():
    """
    POST /api/time_exceptions/early_clock_in

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-07",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = early_clock_in_report(start_date, end_date, user_ids)
    return jsonify(result)


from Reports.time_exception_reports import (
    late_clock_in_report,
    early_clock_out_report,
    early_clock_in_report,
    late_clock_out_report,
)


@time_exceptions_bp.route("/late_clock_out", methods=["POST"])
def get_late_clock_out():
    """
    POST /api/time_exceptions/late_clock_out

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-07",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = late_clock_out_report(start_date, end_date, user_ids)
    return jsonify(result)


@time_exceptions_bp.route("/incomplete_attendance", methods=["POST"])
def get_incomplete_attendance():
    """
    POST /api/time_exceptions/incomplete_attendance

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-07",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = incomplete_attendance_report(start_date, end_date, user_ids)
    return jsonify(result)




@time_exceptions_bp.route("/abscondment", methods=["POST"])
def get_abscondment():
    """
    POST /api/time_exceptions/abscondment

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-07",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = abscondment_report(start_date, end_date, user_ids)
    return jsonify(result)





from Reports.time_exception_reports import (
    late_clock_in_report,
    early_clock_out_report,
    early_clock_in_report,
    late_clock_out_report,
    incomplete_attendance_report,
    abscondment_report,
    low_working_hours_report,
)


@time_exceptions_bp.route("/low_working_hours", methods=["POST"])
def get_low_working_hours():
    """
    POST /api/time_exceptions/low_working_hours

    Body:
    {
        "start_date": "2025-02-01",
        "end_date":   "2025-02-07",
        "user_ids":   ["01141", "01142"]   # optional - omit for all users
    }
    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = low_working_hours_report(start_date, end_date, user_ids)
    return jsonify(result)




from Reports.time_exception_reports import (
    late_clock_in_report,
    early_clock_out_report,
    early_clock_in_report,
    late_clock_out_report,
    incomplete_attendance_report,
    abscondment_report,
    low_working_hours_report,
    meal_punch_only_report,
)


@time_exceptions_bp.route("/meal_punch_only", methods=["POST"])
def get_meal_punch_only():
    """
    POST /api/time_exceptions/meal_punch_only

    """
    body = request.get_json(force=True)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date]):
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = meal_punch_only_report(start_date, end_date, user_ids)
    return jsonify(result)


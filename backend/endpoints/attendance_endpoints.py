
from datetime import datetime, timedelta, date

from flask import Blueprint, jsonify, request

from Reports.attendance_reports import attendance_summary, attendance_by_department, attendance_on_weekends,attendance_on_public_holidays


attendance_bp = Blueprint("attendance", __name__, url_prefix="/api/attendance")


#-------------ATTENDANCE REPORTS-----------------


@attendance_bp.route("/summary", methods=["POST"])
def attendance_summary_route():
    body = request.get_json(force=True)

    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date, user_ids]):
        return jsonify({"error": "start_date, end_date and user_ids are required"}), 400

    result = attendance_summary(start_date, end_date, user_ids)
    return jsonify(result)


@attendance_bp.route("/by-department", methods=["POST"])
def attendance_by_department_route():
    body = request.get_json(force=True)

    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date, user_ids]):
        return jsonify({"error": "start_date, end_date and user_ids are required"}), 400

    result = attendance_by_department(start_date, end_date, user_ids)
    return jsonify(result)


@attendance_bp.route("/weekends", methods=["POST"])
def attendance_on_weekends_route():
    body = request.get_json(force=True)

    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date, user_ids]):
        return jsonify({"error": "start_date, end_date and user_ids are required"}), 400

    result = attendance_on_weekends(start_date, end_date, user_ids)
    return jsonify(result)


@attendance_bp.route("/public-holidays", methods=["POST"])
def attendance_on_public_holidays_route():
    body = request.get_json(force=True)

    start_date = body.get("start_date")
    end_date = body.get("end_date")
    user_ids = body.get("user_ids")

    if not all([start_date, end_date, user_ids]):
        return jsonify({"error": "start_date, end_date and user_ids are required"}), 400

    result = attendance_on_public_holidays(start_date, end_date, user_ids)
    return jsonify(result)

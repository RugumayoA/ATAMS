from flask import Blueprint, jsonify

from Reports.time_exception_reports import (
    get_late_clockin,
    get_early_clockout,
    get_early_clockin,
    get_late_clockout,
    get_incomplete_attendance,
    get_abscondment,
    get_meal_punch_only,
    get_low_working_hours,
)


time_exceptions_bp = Blueprint("time_exceptions", __name__, url_prefix="/api/time_exceptions")


@time_exceptions_bp.route("/late_clockin", methods=["GET"])
def late_clockin():
    return jsonify(get_late_clockin())


@time_exceptions_bp.route("/early_clockout", methods=["GET"])
def early_clockout():
    return jsonify(get_early_clockout())


@time_exceptions_bp.route("/early_clockin", methods=["GET"])
def early_clockin():
    return jsonify(get_early_clockin())


@time_exceptions_bp.route("/late_clockout", methods=["GET"])
def late_clockout():
    return jsonify(get_late_clockout())


@time_exceptions_bp.route("/incomplete_attendance", methods=["GET"])
def incomplete_attendance():
    return jsonify(get_incomplete_attendance())


@time_exceptions_bp.route("/abscondment", methods=["GET"])
def abscondment():
    return jsonify(get_abscondment())


@time_exceptions_bp.route("/meal_punch_only", methods=["GET"])
def meal_punch_only():
    return jsonify(get_meal_punch_only())


@time_exceptions_bp.route("/low_working_hours", methods=["GET"])
def low_working_hours():
    return jsonify(get_low_working_hours())

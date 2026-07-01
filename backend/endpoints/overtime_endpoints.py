from flask import Blueprint, jsonify

from Reports.overtime_reports import (
    get_overtime_summary,
    get_extra_hours_summary,
    get_overtime_vs_extra_hours,
    get_total_mileage_by_employee,
    get_fuel_summary,
)


overtime_bp = Blueprint("overtime", __name__, url_prefix="/api/overtime")


@overtime_bp.route("/summary", methods=["GET"])
def overtime_summary():
    return jsonify(get_overtime_summary())


@overtime_bp.route("/extra-hours", methods=["GET"])
def extra_hours_summary():
    return jsonify(get_extra_hours_summary())


@overtime_bp.route("/overtime-vs-extra-hours", methods=["GET"])
def overtime_vs_extra_hours():
    return jsonify(get_overtime_vs_extra_hours())


@overtime_bp.route("/total-mileage-by-employee", methods=["GET"])
def total_mileage_by_employee():
    return jsonify(get_total_mileage_by_employee())


@overtime_bp.route("/fuel-summary", methods=["GET"])
def fuel_summary():
    return jsonify(get_fuel_summary())

from flask import Blueprint, jsonify

from Reports.shift_reports import (
    get_shift_allocations,
    get_overlapping_shifts,
    get_overlapping_shifts_summary,
)


shifts_bp = Blueprint("shifts", __name__, url_prefix="/api/shifts")


@shifts_bp.route("/allocations", methods=["GET"])
def shift_allocations():
    return jsonify(get_shift_allocations())


@shifts_bp.route("/overlapping", methods=["GET"])
def overlapping_shifts():
    return jsonify(get_overlapping_shifts())


# @shifts_bp.route("/overlapping/summary", methods=["GET"])
# def overlapping_shifts_summary():
#     return jsonify(get_overlapping_shifts_summary())

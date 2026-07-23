"""
endpoints/meals_endpoints.py
Flask routes for the Meals Reports.

Registered in app.py via:
    from endpoints.meals_endpoints import meals_bp
    app.register_blueprint(meals_bp)

All routes take:
    device_id  (required, except /by_device)  - a meal device id
    date       (required)                     - YYYY-MM-DD, interpreted as EAT
"""

from datetime import date, datetime

from flask import Blueprint, jsonify, request

from Reports.meals_report import (
    MEAL_DEVICES,
    daily_meal_punches,
    meal_punches_by_device,
    staff_who_punched,
)

meals_bp = Blueprint("meals", __name__, url_prefix="/api/meals")


# ---------------------------------------------------------------------------
# Shared request parsing
# ---------------------------------------------------------------------------

class BadRequest(Exception):
    """Raised when a query parameter is missing or malformed."""


def _parse_date(raw: str | None) -> date:
    """Parse ?date=YYYY-MM-DD into a date. Defaults to today (EAT)."""
    if not raw:
        raise BadRequest("Missing required parameter: date (YYYY-MM-DD)")
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise BadRequest(f"Invalid date '{raw}'. Expected format YYYY-MM-DD.")


def _parse_device_id(raw: str | None) -> str:
    """Validate ?device_id= against the known meal devices."""
    if not raw:
        raise BadRequest("Missing required parameter: device_id")
    if raw not in MEAL_DEVICES:
        known = ", ".join(f"{k} ({v})" for k, v in MEAL_DEVICES.items())
        raise BadRequest(f"Unknown meal device '{raw}'. Known devices: {known}")
    return raw


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@meals_bp.route("/devices", methods=["GET"])
def get_meal_devices():
    """
    List the meal devices available for reporting.
    Lets the frontend build its device picker without hardcoding ids.

    GET /api/meals/devices
    """
    return jsonify({
        "devices": [
            {"device_id": did, "device_name": name}
            for did, name in MEAL_DEVICES.items()
        ]
    })


@meals_bp.route("/daily_punches", methods=["GET"])
def get_daily_punches():
    """
    Every meal punch on one device for one EAT day. One row per punch.

    GET /api/meals/daily_punches?device_id=939276804&date=2026-07-21
    """
    try:
        device_id = _parse_device_id(request.args.get("device_id"))
        day = _parse_date(request.args.get("date"))
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    try:
        return jsonify(daily_meal_punches(device_id, day))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch meal punches: {e}"}), 502


@meals_bp.route("/staff_by_device", methods=["GET"])
def get_staff_by_device():
    """
    Distinct staff who punched at one device on one EAT day.
    One row per person, with punch count and times.

    GET /api/meals/staff_by_device?device_id=939276804&date=2026-07-21
    """
    try:
        device_id = _parse_device_id(request.args.get("device_id"))
        day = _parse_date(request.args.get("date"))
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    try:
        return jsonify(staff_who_punched(device_id, day))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch staff meal report: {e}"}), 502


@meals_bp.route("/by_device", methods=["GET"])
def get_by_device():
    """
    Totals for every meal device on one EAT day.
    No device_id: this covers all of them.

    GET /api/meals/by_device?date=2026-07-21
    """
    try:
        day = _parse_date(request.args.get("date"))
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    try:
        return jsonify(meal_punches_by_device(day))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch device summary: {e}"}), 502
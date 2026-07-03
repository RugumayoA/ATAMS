from flask import Blueprint, jsonify

from Reports.meals_report import get_meals_summary


meals_bp = Blueprint("meals", __name__, url_prefix="/api/meals")


@meals_bp.route("/summary", methods=["GET"])
def meals_summary():
    return jsonify(get_meals_summary())

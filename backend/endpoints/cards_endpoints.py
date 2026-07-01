from flask import Blueprint, jsonify

from Reports.cards import (
    get_card_status,
    get_staff_assigned_to_cards,
    get_blacklisted_cards,
    get_denied_cards,
)


cards_bp = Blueprint("cards", __name__, url_prefix="/api/cards")


@cards_bp.route("/status", methods=["GET"])
def card_status():
    return jsonify(get_card_status())


@cards_bp.route("/assigned", methods=["GET"])
def staff_assigned_to_cards():
    return jsonify(get_staff_assigned_to_cards())


@cards_bp.route("/blacklisted", methods=["GET"])
def blacklisted_cards():
    return jsonify(get_blacklisted_cards())


@cards_bp.route("/denied", methods=["GET"])
def denied_cards():
    return jsonify(get_denied_cards())

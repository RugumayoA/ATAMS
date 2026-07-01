from flask import Blueprint, jsonify

from Reports.user_reports import (
    get_all_users,
    get_new_users,
    get_users_no_credentials,
    get_users_by_category,
    get_expiring_soon,
    get_users_on_device,
    get_exceptional_users,
)


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/all", methods=["GET"])
def all_users():
    return jsonify(get_all_users())


@users_bp.route("/new", methods=["GET"])
def new_users():
    return jsonify(get_new_users())


@users_bp.route("/no-credentials", methods=["GET"])
def users_no_credentials():
    return jsonify(get_users_no_credentials())


@users_bp.route("/category/<category>", methods=["GET"])
def users_by_category(category):
    return jsonify(get_users_by_category(category))


@users_bp.route("/expiring-soon", methods=["GET"])  # supposed to be exceptional users and we change when we get the real data
def expiring_soon():
    return jsonify(get_expiring_soon())


@users_bp.route("/active", methods=["GET"])
def active_devices():
    return jsonify(get_users_on_device())


@users_bp.route("/exceptional", methods=["GET"])
def exceptional_users():
    return jsonify(get_exceptional_users())

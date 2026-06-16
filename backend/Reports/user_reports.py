from flask import Flask,jsonify,request
from flask_cors import CORS 
from mockdata import employees, attendence_records, shift_allocations
app=Flask(__name__)
CORS(app)

#.....user reports........
@app.route("/api/users/all", methods=["GET"])
def get_all_users():
    return jsonify(employees)

@app.route("/api/users/new", methods=["GET"])
def get_new_users():
    new_users = [e for e in employees if e["is_new_user"]]
    return jsonify(new_users)

@app.route("/api/users/no-credentials", methods=["GET"])
def get_users_no_credentials():
    no_creds = [e for e in employees if not e["has_credentials"]]
    return jsonify(no_creds)

@app.route("/api/users/expiring-soon", methods=["GET"])
def get_expiring_soon():
    from datetime import datetime
    today = datetime.today()
    expiring = [
        e for e in employees
        if (datetime.strptime(e["account_expiry"], "%Y-%m-%d") - today).days <= 30
    ]
    return jsonify(expiring)

@app.route("/api/users/by-category", methods=["GET"])
def get_users_by_category():
    categories = {}
    for e in employees:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(e)
    return jsonify(categories)

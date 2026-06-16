from flask import Flask, jsonify

app = Flask(__name__)

# Mock data
employees = []  # Load from database or mock data
attendance_records = []  # Load from database or mock data
@app.route("/api/attendance/by-department", methods=["GET"])
def get_attendance_by_department():
    dept_map = {e["user_id"]: e["department"] for e in employees}
    departments = {}
    for r in attendance_records:
        dept = dept_map.get(r["user_id"], "Unknown")
        if dept not in departments:
            departments[dept] = {"present": 0, "absent": 0}
        if r["check_in"]:
            departments[dept]["present"] += 1
        else:
            departments[dept]["absent"] += 1
    return jsonify(departments)

@app.route("/api/attendance/public-holidays", methods=["GET"])
def get_public_holiday_attendance():
    ph = [r for r in attendance_records if r["is_public_holiday"]]
    return jsonify(ph)

@app.route("/api/attendance/weekends", methods=["GET"])
def get_weekend_attendance():
    weekends = [r for r in attendance_records if r["is_weekend"]]
    return jsonify(weekends)

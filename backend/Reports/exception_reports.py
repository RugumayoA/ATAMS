from flask import Flask, jsonify, request
from flask_cors import CORS
from mockdata import employees, attendance_records, shift_allocations

app = Flask(__name__)
CORS(app)


# ── TIME-BASED EXCEPTION REPORTS ─────────────────────────

@app.route("/api/exceptions/late-clockout", methods=["GET"])
def get_late_clockout():
    late_out = [
        r for r in attendance_records
        if r["check_out"] and r["check_out"] > r["shift_end"]
    ]
    return jsonify(late_out)
@app.route("/api/exceptions/late-clockin", methods=["GET"])
def get_late_clockin():
    late = [
        r for r in attendance_records
        if r["check_in"] and r["check_in"] > r["shift_start"]
    ]
    return jsonify(late)

@app.route("/api/exceptions/early-clockout", methods=["GET"])
def get_early_clockout():
    early_out = [
        r for r in attendance_records
        if r["check_out"] and r["check_out"] < r["shift_end"]
    ]
    return jsonify(early_out)

@app.route("/api/exceptions/early-clockin", methods=["GET"])
def get_early_clockin():
    early_in = [
        r for r in attendance_records
        if r["check_in"] and r["check_in"] < r["shift_start"]
    ]
    return jsonify(early_in)

@app.route("/api/exceptions/incomplete", methods=["GET"])
def get_incomplete_attendance():
    incomplete = [
        r for r in attendance_records
        if r["check_in"] and not r["check_out"]
    ]
    return jsonify(incomplete)

@app.route("/api/exceptions/abscondment", methods=["GET"])
def get_abscondment():
    absconded = [r for r in attendance_records if r["abscondment"]]
    return jsonify(absconded)
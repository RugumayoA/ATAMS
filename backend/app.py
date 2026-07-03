from flask import Flask, jsonify
from flask_cors import CORS

from endpoints.users_endpoints import users_bp
from endpoints.cards_endpoints import cards_bp
from endpoints.attendance_endpoints import attendance_bp
from endpoints.time_exceptions_endpoints import time_exceptions_bp
from endpoints.shifts_endpoints import shifts_bp
from endpoints.leave_endpoints import leave_bp
from endpoints.meals_endpoints import meals_bp
from endpoints.overtime_endpoints import overtime_bp


app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(time_exceptions_bp)
app.register_blueprint(shifts_bp)
app.register_blueprint(leave_bp)
app.register_blueprint(meals_bp)
app.register_blueprint(overtime_bp)


@app.route("/")
def home():
    return jsonify({"message": "ATAMS Backend is running!"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

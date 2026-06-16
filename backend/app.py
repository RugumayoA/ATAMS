from flask import Flask, jsonify
from flask_cors import CORS

from Reports.user_reports import (
    get_all_users,
    get_new_users,
    get_users_no_credentials,
    get_users_by_category,
    get_expiring_soon,
    get_users_on_device,
    get_exceptional_users
)


app = Flask(__name__) #create a Flask application instance
CORS(app)             # disables cross-origin sharing restrictions  allowing frontend to communicate with backed

@app.route("/") #register a route for the root URL ("/") of the applrsication
def home():
    return jsonify({"message": "ATAMS Backend is running!"})



#-------------USER REPORTS-----------------
@app.route("/api/users/all")
def all_users():
    return jsonify(get_all_users())

@app.route("/api/users/new")
def new_users():
    return jsonify(get_new_users())

@app.route("/api/users/no-credentials")
def users_no_credentials():
    return jsonify(get_users_no_credentials())

@app.route("/api/users/category/<category>")
def users_by_category(category):
    return jsonify(get_users_by_category(category))

@app.route("/api/users/expiring-soon") # supposed to be exceptional users and we change when we get the real data
def expiring_soon():
    return jsonify(get_expiring_soon())

@app.route("/api/users/active")
def active_devices():
    return jsonify(get_users_on_device())

@app.route("/api/users/exceptional")
def exceptional_users():
    return jsonify(get_exceptional_users()) 





if __name__ == "__main__":      #starts app when you run python app.py 
    app.run(debug=True, port=5000)
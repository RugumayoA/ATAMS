from flask import Flask, jsonify
from flask_cors import CORS

from reports.user_reports import (
    get_all_users,
    get_new_users,
    get_users_without_credentials,
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







if __name__ == "__main__":      #starts app when you run python app.py 
    app.run(debug=True, port=5000)
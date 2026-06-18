from flask import Flask, jsonify
from flask_cors import CORS

from Reports.user_reports import (get_all_users,get_new_users,get_users_no_credentials,get_users_by_category,get_expiring_soon, get_users_on_device,get_exceptional_users)
from Reports.attendance_reports import (get_attendance_summary,get_attendance_by_department,get_public_holiday_attendance,get_weekend_attendance)
from Reports.time_exception_reports import (get_late_clockin,get_early_clockout,get_early_clockin,get_late_clockout,get_incomplete_attendance,get_abscondment,get_meal_punch_only,get_low_working_hours)
from Reports.shift_reports import (get_shift_allocations,get_overlapping_shifts,get_overlapping_shifts_summary)
#from Reports.overtime_reports import (get_overtime_summary,get_extra_hours_summary,get_overtime_vs_extra_hours)
from Reports.leave_reports import (get_staff_on_leave,get_leave_reconciliation)



app = Flask(__name__) #create a Flask application instance
CORS(app)             # disables cross-origin sharing restrictions  allowing frontend to communicate with backed

@app.route("/") #register a route for the root URL ("/") of the applrsication
def home():
    return jsonify({"message": "ATAMS Backend is running!"})



#-------------USER REPORTS-----------------
@app.route("/api/users/all", methods=["GET"])
def all_users():
    return jsonify(get_all_users())

@app.route("/api/users/new",  methods=["GET"])
def new_users():
    return jsonify(get_new_users())

@app.route("/api/users/no-credentials", methods=["GET"])
def users_no_credentials():
    return jsonify(get_users_no_credentials())

@app.route("/api/users/category/<category>", methods=["GET"])
def users_by_category(category):
    return jsonify(get_users_by_category(category))

@app.route("/api/users/expiring-soon", methods=["GET"]) # supposed to be exceptional users and we change when we get the real data
def expiring_soon():
    return jsonify(get_expiring_soon())

@app.route("/api/users/active", methods=["GET"])
def active_devices():
    return jsonify(get_users_on_device())

@app.route("/api/users/exceptional", methods=["GET"])
def exceptional_users():
    return jsonify(get_exceptional_users()) 



#-------------ATTENDANCE REPORTS-----------------
@app.route("/api/attendance/summary", methods=["GET"])
def attendance_summary():
    return jsonify(get_attendance_summary())    

@app.route("/api/attendance/department", methods=["GET"])
def attendance_by_department():
    return jsonify(get_attendance_by_department())

@app.route("/api/attendance/public-holiday", methods=["GET"])
def public_holiday_attendance():
    return jsonify(get_public_holiday_attendance()) 

@app.route("/api/attendance/weekend", methods=["GET"])
def weekend_attendance():
    return jsonify(get_weekend_attendance())



#---------------TIME EXCEPTION REPORTS-----------------
@app.route("/api/time_exceptions/late_clockin", methods=["GET"])
def late_clockin():
    return jsonify(get_late_clockin())

@app.route("/api/time_exceptions/early_clockout", methods=["GET"])
def early_clockout():
    return jsonify(get_early_clockout())

@app.route("/api/time_exceptions/early_clockin", methods=["GET"])
def early_clockin():
    return jsonify(get_early_clockin())

@app.route("/api/time_exceptions/late_clockout", methods=["GET"])
def late_clockout():
    return jsonify(get_late_clockout())

@app.route("/api/time_exceptions/incomplete_attendance", methods=["GET"])
def incomplete_attendance():    
    return jsonify(get_incomplete_attendance())     

@app.route("/api/time_exceptions/abscondment", methods=["GET"])
def abscondment():  
    return jsonify(get_abscondment())       

@app.route("/api/time_exceptions/meal_punch_only", methods=["GET"])
def meal_punch_only():  
    return jsonify(get_meal_punch_only())   

@app.route("/api/time_exceptions/low_working_hours", methods=["GET"])
def low_working_hours():  
    return jsonify(get_low_working_hours())  


#-------------SHIFT REPORTS-----------------
@app.route("/api/shifts/allocations", methods=["GET"])
def shift_allocations():
    return jsonify(get_shift_allocations())

@app.route("/api/shifts/overlapping", methods=["GET"])
def overlapping_shifts():
    return jsonify(get_overlapping_shifts())

'''@app.route("/api/shifts/overlapping/summary", methods=["GET"])
def overlapping_shifts_summary():
    return jsonify(get_overlapping_shifts_summary())'''



#-------------LEAVE REPORTS-----------------
@app.route("/api/leave/staff-on-leave", methods=["GET"])
def staff_on_leave():
    return jsonify(get_staff_on_leave())

@app.route("/api/leave/reconciliation", methods=["GET"])
def leave_reconciliation():
    return jsonify(get_leave_reconciliation())  



if __name__ == "__main__":      #starts app when you run python app.py 
    app.run(debug=True, port=5000)
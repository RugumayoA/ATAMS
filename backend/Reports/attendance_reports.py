from mockdata import employees, attendance_records

emp_map = {e["user_id"]: e for e in employees}

def _staff(user_id):
    emp = emp_map.get(user_id, {})
    return {
        "employee_id": user_id,
        "name":        emp.get("name", "—"),
        "card_id":     emp.get("card_id", "—"),
    }

def get_attendance_summary():
    present  = [r for r in attendance_records if r["check_in"] and not r["on_leave"]]
    absent   = [r for r in attendance_records if not r["check_in"] and not r["on_leave"]]
    on_leave = [r for r in attendance_records if r["on_leave"]]
    return {
        "total":           len(attendance_records),
        "present":         len(present),
        "absent":          len(absent),
        "on_leave":        len(on_leave),
        "all_records":     [_staff(r["user_id"]) for r in attendance_records],
        "present_records": [_staff(r["user_id"]) for r in present],
        "absent_records":  [_staff(r["user_id"]) for r in absent],
        "on_leave_records":[_staff(r["user_id"]) for r in on_leave],
    }

def get_attendance_by_department():
    dept_map = {e["user_id"]: e["department"] for e in employees}

    def _staff_with_dept(r):
        s = _staff(r["user_id"])
        s["department"] = dept_map.get(r["user_id"], "Unknown")
        return s

    present  = [r for r in attendance_records if r["check_in"] and not r["on_leave"]]
    absent   = [r for r in attendance_records if not r["check_in"] and not r["on_leave"]]
    on_leave = [r for r in attendance_records if r["on_leave"]]

    return {
        "total":           len(attendance_records),
        "present":         len(present),
        "absent":          len(absent),
        "on_leave":        len(on_leave),
        "all_records":     [_staff_with_dept(r) for r in attendance_records],
        "present_records": [_staff_with_dept(r) for r in present],
        "absent_records":  [_staff_with_dept(r) for r in absent],
        "on_leave_records":[_staff_with_dept(r) for r in on_leave],
    }

def get_public_holiday_attendance():
    return [_staff(r["user_id"]) for r in attendance_records if r["is_public_holiday"]]

def get_weekend_attendance():
    return [_staff(r["user_id"]) for r in attendance_records if r["is_weekend"]]

from mock_data import employees, attendance_records

def get_attendance_summary():
    present  = [r for r in attendance_records if r["check_in"]]
    absent   = [r for r in attendance_records if not r["check_in"] and not r["on_leave"]]
    on_leave = [r for r in attendance_records if r["on_leave"]]
    return {
        "total":    len(attendance_records),
        "present":  len(present),
        "absent":   len(absent),
        "on_leave": len(on_leave)
    }

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
    return departments

def get_public_holiday_attendance():
    return [r for r in attendance_records if r["is_public_holiday"]]

def get_weekend_attendance():
    return [r for r in attendance_records if r["is_weekend"]]

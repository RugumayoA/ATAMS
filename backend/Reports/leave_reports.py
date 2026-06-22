from mockdata import attendance_records, employees

_emp_lookup = {e["user_id"]: e for e in employees}


def get_staff_on_leave():
    return [
        {
            "employee_name": _emp_lookup.get(r["user_id"], {}).get("name", "Unknown"),
            "user_id":       r["user_id"],
            "department":    _emp_lookup.get(r["user_id"], {}).get("department", "Unknown"),
            "date":          r["date"],
            "shift":         r["shift"],
        }
        for r in attendance_records if r["on_leave"]
    ]


def get_leave_reconciliation():
    """
    Get anomalies: staff marked on leave but still clocked in.
    Returns: List of records where on_leave=True but check_in exists.
    """
    return [
        {
            "employee_name": _emp_lookup.get(r["user_id"], {}).get("name", "Unknown"),
            "user_id":       r["user_id"],
            "date":          r["date"],
            "shift":         r["shift"],
            "check_in":      r["check_in"],
            "check_out":     r["check_out"],
            "status":        "ANOMALY - On Leave but Clocked In"
        }
        for r in attendance_records
        if r["on_leave"] and r["check_in"]
    ]




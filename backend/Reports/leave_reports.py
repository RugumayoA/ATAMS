from mockdata import attendance_records


def get_staff_on_leave():
    """
    Get all staff marked as on leave.
    Returns: List of leave records with user_id, date, shift, and leave status.
    """
    return [
        {
            "user_id": r["user_id"],
            "date": r["date"],
            "shift": r["shift"],
            "on_leave": r["on_leave"]
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
            "user_id": r["user_id"],
            "date": r["date"],
            "shift": r["shift"],
            "on_leave": r["on_leave"],
            "check_in": r["check_in"],
            "check_out": r["check_out"],
            "status": "ANOMALY - On Leave but Clocked In"
        }
        for r in attendance_records
        if r["on_leave"] and r["check_in"]
    ]


def get_leave_summary():
    """
    Get a summary of leave by date.
    Returns: Dictionary with date as key and list of staff on leave.
    """
    leave_by_date = {}
    
    for r in attendance_records:
        if r["on_leave"]:
            date = r["date"]
            if date not in leave_by_date:
                leave_by_date[date] = []
            leave_by_date[date].append({
                "user_id": r["user_id"],
                "shift": r["shift"]
            })
    
    return leave_by_date

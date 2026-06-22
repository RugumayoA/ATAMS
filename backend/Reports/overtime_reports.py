from mockdata import attendance_records, mileage_records, fuel_records, employees

_name_lookup = {e["user_id"]: e["name"] for e in employees}


def _to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def _calc_overtime_hours(r):
    if r["check_in"] is None or r["check_out"] is None:
        return 0

    shift_start = _to_minutes(r["shift_start"])
    shift_end   = _to_minutes(r["shift_end"])
    check_in    = _to_minutes(r["check_in"])
    check_out   = _to_minutes(r["check_out"])

    # Handle overnight shifts and overnight check-out
    if shift_end <= shift_start:
        shift_end += 24 * 60
    if check_out <= check_in:
        check_out += 24 * 60

    shift_duration = shift_end - shift_start
    worked         = check_out - check_in

    return round(max(0, worked - shift_duration) / 60, 2)


def get_overtime_summary():
    results = []
    for r in attendance_records:
        ot_minutes = _calc_overtime_hours(r)
        if ot_minutes > 0:
            results.append({
                "employee_name":    _name_lookup.get(r["user_id"], "Unknown"),
                "user_id":          r["user_id"],
                "check_in":         r["check_in"],
                "check_out":        r["check_out"],
                "shift_start":      r["shift_start"],
                "shift_end":        r["shift_end"],
                "overtime_hours": ot_minutes,
            })
    return results


def get_extra_hours_summary():
    results = []
    for r in attendance_records:
        ot_minutes = _calc_overtime_hours(r)
        if ot_minutes > 0:
            results.append({
                "employee_name":    _name_lookup.get(r["user_id"], "Unknown"),
                "user_id":          r["user_id"],
                "check_in":         r["check_in"],
                "check_out":        r["check_out"],
                "shift_start":      r["shift_start"],
                "shift_end":        r["shift_end"],
                "overtime_hours": ot_minutes,
            })
    return results


def get_overtime_vs_extra_hours():
    results = []
    for r in attendance_records:
        ot_minutes = _calc_overtime_hours(r)
        if ot_minutes > 0:
            results.append({
                "employee_name":    _name_lookup.get(r["user_id"], "Unknown"),
                "user_id":          r["user_id"],
                "overtime_hours": ot_minutes,
            })
    return results


def get_total_mileage_by_employee():
    mileage_by_employee = {}
    for record in mileage_records:
        user_id = record["user_id"]
        if user_id not in mileage_by_employee:
            mileage_by_employee[user_id] = {"user_id": user_id, "total_miles": 0, "trips": 0}
        mileage_by_employee[user_id]["total_miles"] += record["total_miles"]
        mileage_by_employee[user_id]["trips"] += 1
    return list(mileage_by_employee.values())


def get_fuel_summary():
    return fuel_records

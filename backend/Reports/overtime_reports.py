from mockdata import attendance_records, mileage_records, fuel_records


def get_overtime_summary():
    return [r for r in attendance_records if r["overtime_hours"] > 0]


def get_extra_hours_summary():
    return [r for r in attendance_records if r["extra_hours"] > 0]


def get_overtime_vs_extra_hours():
    return [
        {
"user_id":        r["user_id"],
"overtime_hours": r["overtime_hours"],
"extra_hours":    r["extra_hours"]
        }
        for r in attendance_records
        if r["overtime_hours"] > 0 or r["extra_hours"] > 0
    ]


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


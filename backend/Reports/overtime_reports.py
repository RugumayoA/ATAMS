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

'''def get_mileage_summary():
    return mileage_records'''


def get_total_mileage_by_employee():
    mileage_by_employee = {}
    for record in mileage_records:
        user_id = record["user_id"]
        if user_id not in mileage_by_employee:
            mileage_by_employee[user_id] = {"user_id": user_id, "total_miles": 0, "trips": 0}
        mileage_by_employee[user_id]["total_miles"] += record["total_miles"]
        mileage_by_employee[user_id]["trips"] += 1
    return list(mileage_by_employee.values())


def get_mileage_by_vehicle():
    mileage_by_vehicle = {}
    for record in mileage_records:
        vehicle_id = record["vehicle_id"]
        if vehicle_id not in mileage_by_vehicle:
            mileage_by_vehicle[vehicle_id] = {"vehicle_id": vehicle_id, "total_miles": 0, "trips": 0}
        mileage_by_vehicle[vehicle_id]["total_miles"] += record["total_miles"]
        mileage_by_vehicle[vehicle_id]["trips"] += 1
    return list(mileage_by_vehicle.values())


def get_mileage_by_purpose():
    mileage_by_purpose = {}
    for record in mileage_records:
        purpose = record["purpose"]
        if purpose not in mileage_by_purpose:
            mileage_by_purpose[purpose] = {"purpose": purpose, "total_miles": 0, "trips": 0}
        mileage_by_purpose[purpose]["total_miles"] += record["total_miles"]
        mileage_by_purpose[purpose]["trips"] += 1
    return list(mileage_by_purpose.values())


def get_fuel_summary():
    return fuel_records


def get_total_fuel_expense_by_employee():
    fuel_by_employee = {}
    for record in fuel_records:
        user_id = record["user_id"]
        if user_id not in fuel_by_employee:
            fuel_by_employee[user_id] = {"user_id": user_id, "total_fuel_liters": 0, "total_amount_spent": 0, "fuel_transactions": 0}
        fuel_by_employee[user_id]["total_fuel_liters"] += record["liters_filled"]
        fuel_by_employee[user_id]["total_amount_spent"] += record["amount_spent"]
        fuel_by_employee[user_id]["fuel_transactions"] += 1
    return list(fuel_by_employee.values())


''''def get_fuel_by_vehicle():
    fuel_by_vehicle = {}
    for record in fuel_records:
        vehicle_id = record["vehicle_id"]
        if vehicle_id not in fuel_by_vehicle:
            fuel_by_vehicle[vehicle_id] = {"vehicle_id": vehicle_id, "total_fuel_liters": 0, "total_amount_spent": 0, "fuel_transactions": 0}
        fuel_by_vehicle[vehicle_id]["total_fuel_liters"] += record["liters_filled"]
        fuel_by_vehicle[vehicle_id]["total_amount_spent"] += record["amount_spent"]
        fuel_by_vehicle[vehicle_id]["fuel_transactions"] += 1
    return list(fuel_by_vehicle.values())'''


''''def get_fuel_by_type():
    fuel_by_type = {}
    for record in fuel_records:
        fuel_type = record["fuel_type"]
        if fuel_type not in fuel_by_type:
            fuel_by_type[fuel_type] = {"fuel_type": fuel_type, "total_liters": 0, "total_spent": 0, "transactions": 0}
        fuel_by_type[fuel_type]["total_liters"] += record["liters_filled"]
        fuel_by_type[fuel_type]["total_spent"] += record["amount_spent"]
        fuel_by_type[fuel_type]["transactions"] += 1
    return list(fuel_by_type.values())'''


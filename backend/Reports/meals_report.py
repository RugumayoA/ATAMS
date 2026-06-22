from mockdata import attendance_records, employees

_name_lookup = {e["user_id"]: e["name"] for e in employees}


def get_meals_summary():
    meals    = [r for r in attendance_records if r["meal_punch"]]
    accepted = [r for r in meals if r["meal_accepted"]]
    denied   = [r for r in meals if not r["meal_accepted"]]
    records  = [
        {
            "employee_name": _name_lookup.get(r["user_id"], "Unknown"),
            "user_id":       r["user_id"],
            "date":          r["date"],
            "shift":         r["shift"],
            "meal_punch":    r["meal_punch"],
            "meal_accepted": r["meal_accepted"],
        }
        for r in meals
    ]
    return {
        "total_meal_punches": len(meals),
        "accepted":           len(accepted),
        "denied":             len(denied),
        "records":            records
    }
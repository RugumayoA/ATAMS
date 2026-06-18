from mockdata import attendance_records


def get_meals_summary():
    meals    = [r for r in attendance_records if r["meal_punch"]]
    accepted = [r for r in meals if r["meal_accepted"]]
    denied   = [r for r in meals if not r["meal_accepted"]]
    return {
        "total_meal_punches": len(meals),
        "accepted":           len(accepted),
        "denied":             len(denied),
        "records":            meals
    }
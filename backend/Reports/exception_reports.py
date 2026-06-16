from mockdata import attendance_records


def get_late_clockin():
    return [
        r for r in attendance_records
        if r["check_in"] and r["check_in"] > r["shift_start"]
    ]


def get_early_clockout():
    return [
        r for r in attendance_records
        if r["check_out"] and r["check_out"] < r["shift_end"]
    ]


def get_early_clockin():
    return [
        r for r in attendance_records
        if r["check_in"] and r["check_in"] < r["shift_start"]
    ]


def get_late_clockout():
    return [
        r for r in attendance_records
        if r["check_out"] and r["check_out"] > r["shift_end"]
    ]


def get_incomplete_attendance():
    return [
        r for r in attendance_records
        if r["check_in"] and not r["check_out"]
    ]


def get_abscondment():
    return [r for r in attendance_records if r["abscondment"]]


def get_meal_punch_only():
    return [
        r for r in attendance_records
        if r["meal_punch"] and not r["check_in"]
    ]


def get_low_working_hours(min_hours=8):
    low = []
    for r in attendance_records:
        if r["check_in"] and r["check_out"]:
            fmt = "%H:%M"
            from datetime import datetime
            start = datetime.strptime(r["check_in"],  fmt)
            end   = datetime.strptime(r["check_out"], fmt)
            hours = (end - start).seconds / 3600
            if hours < min_hours:
                r["hours_worked"] = round(hours, 2)
                low.append(r)
    return low

from mock_data import attendance_records


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


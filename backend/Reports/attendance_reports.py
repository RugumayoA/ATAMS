from biostar_connector import fetch_daily_attendance
from datetime import datetime, timedelta


def attendance_summary(start_date, end_date, user_ids):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    present = []
    absent = []

    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        data = fetch_daily_attendance(date_str, date_str, user_ids)
        records = data.get("records", [])

        for record in records:
            record["date"] = date_str
            if record["inTime"] != "-":
                present.append(record)
            else:
                absent.append(record)

        current += timedelta(days=1)

    return {
        "present_count": len(present),
        "absent_count": len(absent),
        "present": present,
        "absent": absent,
    }


def attendance_by_department(start_date, end_date, user_ids):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    departments = {}

    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        data = fetch_daily_attendance(date_str, date_str, user_ids)
        records = data.get("records", [])

        for record in records:
            record["date"] = date_str
            dept = record["userGroupName"]

            if dept not in departments:
                departments[dept] = {"present": [], "absent": []}

            if record["inTime"] != "-":
                departments[dept]["present"].append(record)
            else:
                departments[dept]["absent"].append(record)

        current += timedelta(days=1)

    summary = {}
    for dept, groups in departments.items():
        summary[dept] = {
            "present_count": len(groups["present"]),
            "absent_count": len(groups["absent"]),
            "present": groups["present"],
            "absent": groups["absent"],
        }

    return summary


def attendance_on_weekends(start_date, end_date, user_ids):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    weekend_dates = []
    current = start
    while current <= end:
        if current.weekday() in (5, 6):  # 5 = Saturday, 6 = Sunday
            weekend_dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    results = {}
    for date in weekend_dates:
        data = fetch_daily_attendance(date, date, user_ids)
        records = data.get("records", [])
        for record in records:
            record["date"] = date

        present = [r for r in records if r["inTime"] != "-"]
        absent  = [r for r in records if r["inTime"] == "-"]

        results[date] = {
            "present_count": len(present),
            "absent_count": len(absent),
            "present": present,
            "absent": absent,
        }

    return results


PUBLIC_HOLIDAYS_2025 = [
    "2025-01-01",  # New Year's Day
    "2025-01-26",  # Liberation Day
    "2025-03-08",  # Women's Day
    "2025-04-18",  # Good Friday
    "2025-04-21",  # Easter Monday
    "2025-05-01",  # Labour Day
    "2025-06-03",  # Martyrs Day
    "2025-06-09",  # Heroes Day
    "2025-10-09",  # Independence Day
    "2025-12-25",  # Christmas Day
    "2025-12-26",  # Boxing Day
]


def attendance_on_public_holidays(start_date, end_date, user_ids):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    holidays_in_range = [
        h for h in PUBLIC_HOLIDAYS_2025
        if start <= datetime.strptime(h, "%Y-%m-%d") <= end
    ]

    if not holidays_in_range:
        return {"message": "No public holidays in the selected date range", "results": {}}

    results = {}

    
    for date in holidays_in_range:
        data = fetch_daily_attendance(date, date, user_ids)
        records = data.get("records", [])
        for record in records:
            record["date"] = date

        present = [r for r in records if r["inTime"] != "-"]
        absent  = [r for r in records if r["inTime"] == "-"]

        results[date] = {
            "present_count": len(present),
            "absent_count":  len(absent),
            "present": present,
            "absent":  absent,
        }

    return results
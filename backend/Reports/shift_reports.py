from mockdata import shift_allocations, employees
from collections import Counter

_name_lookup = {e["user_id"]: e["name"] for e in employees}


def get_shift_allocations():
    """
    Get all shift allocations with their schedule templates.
    Returns: List of allocations with user_id, employee_name, shift, and schedule_template.
    """
    return [
        {
            "user_id": s["user_id"],
            "employee_name": _name_lookup.get(s["user_id"], "Unknown"),
            "shift": s["shift"],
            "schedule_template": s["schedule_template"]
        }
        for s in shift_allocations
    ]


def get_overlapping_shifts():
    """
    Get staff with overlapping shifts or multiple schedules.
    Returns: List of records for staff assigned to more than one shift/schedule.
    """
    user_counts = Counter(s["user_id"] for s in shift_allocations)
    return [
        {
            "user_id": s["user_id"],
            "employee_name": _name_lookup.get(s["user_id"], "Unknown"),
            "shift": s["shift"],
            "schedule_template": s["schedule_template"]
        }
        for s in shift_allocations
        if user_counts[s["user_id"]] > 1
    ]


def get_overlapping_shifts_summary():
    """
    Get a summary of staff with overlapping shifts, grouped by user.
    Returns: Dictionary with user_id as key and list of shifts/schedules as value.
    """
    user_counts = Counter(s["user_id"] for s in shift_allocations)
    overlapping_summary = {}
    
    for user_id in [uid for uid, count in user_counts.items() if count > 1]:
        overlapping_summary[user_id] = [
            {
                "shift": s["shift"],
                "schedule_template": s["schedule_template"]
            }
            for s in shift_allocations if s["user_id"] == user_id
        ]
    
    return overlapping_summary


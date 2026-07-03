# backend/time_exception_reports.py
"""
Time Exception Reports
=======================
Built entirely from the Daily Attendance API (same one used by attendance_reports.py) -
no separate Biostar endpoint needed. Each daily attendance record carries an
`exception` field that can hold MULTIPLE exception types in one comma-separated
string, e.g.:

    "Late In"
    "Late In, Early Out"
    "Insufficient work time, Missing Punch Out, Late In"
    "-"   (means no exceptions - a clean shift)

Because of this, we match with substring containment (`keyword in exception_string`)
rather than exact equality (`==`), so a record with two exceptions correctly shows
up under both matching reports.

NOTE on unreliable boolean flags: real data shows fields like `missingPunchOut`
and `absence` staying `false` even when the `exception` string clearly says
"Missing Punch Out" or "Absence". Same pattern we found in attendance_reports.py.
Always trust the `exception` STRING field, never the boolean flags.
"""

from biostar_connector import fetch_daily_attendance

# Maps each frontend tab -> the exact substring to look for inside `exception`.
#
# CONFIRMED against real API data:
#   "Late In", "Early Out", "Absence", "Missing Punch Out", "Insufficient work time"
#
# NOT YET CONFIRMED (no real example seen so far) - built on the assumed
# symmetric naming pattern. Verify the real spelling once you see a live
# example, then update here if it differs:
EXCEPTION_KEYWORDS = {
    "late_clock_in":         "Late In",
    "early_clock_out":       "Early Out",
    "early_clock_in":        "Early In",             # UNVERIFIED - assumed spelling
    "late_clock_out":        "Late Out",              # UNVERIFIED - assumed spelling
    "incomplete_attendance": "Missing Punch Out",
    "abscondment":           "Absence",
    "low_working_hours":     "Insufficient work time",
}

# "Meal Punch Only" has no known basis in the Daily Attendance API - every
# record seen so far with inTime == "-" also has mealTime == "-". Left as a
# placeholder returning empty results until we find out what data source
# (a different Biostar endpoint? a different field?) actually defines it.
PLACEHOLDER_TABS = {"meal_punch_only"}


def time_exception_report(exception_keyword, start_date, end_date, user_ids=None):
    """
    Core filter. Pulls daily attendance for the given date range (and
    optional user_ids list), then returns only the records whose `exception`
    field contains exception_keyword as a substring.
    """
    data = fetch_daily_attendance(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        r for r in records
        if exception_keyword in r.get("exception", "")
    ]

    return {
        "exception_type": exception_keyword,
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }


def time_exception_by_tab(tab, start_date, end_date, user_ids=None):
    """
    Looks up a frontend tab name (e.g. "late_clock_in", "abscondment") and
    runs the matching report. Returns an empty placeholder result for tabs
    we can't yet compute (currently just "meal_punch_only").

    Raises ValueError for an unrecognized tab name.
    """
    if tab in PLACEHOLDER_TABS:
        return {
            "exception_type": tab,
            "start_date": start_date,
            "end_date": end_date,
            "total": 0,
            "records": [],
            "note": "Not yet derivable from the Daily Attendance API - placeholder pending data source confirmation.",
        }

    keyword = EXCEPTION_KEYWORDS.get(tab)
    if keyword is None:
        raise ValueError(
            f"Unknown time exception tab: '{tab}'. "
            f"Valid tabs: {sorted(list(EXCEPTION_KEYWORDS.keys()) + list(PLACEHOLDER_TABS))}"
        )

    return time_exception_report(keyword, start_date, end_date, user_ids)

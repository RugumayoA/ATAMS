# backend/Reports/time_exception_reports.py
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
"Missing Punch Out" or "Absence". Always trust the `exception` STRING field,
never the boolean flags.

NOTE on dates: Biostar's Daily Attendance API does NOT return a date field
per record, even for multi-day queries (confirmed against a real 423-record
multi-day response with zero date-like fields). We use
fetch_daily_attendance_range, which loops day-by-day internally and manually
stamps a "date" field onto every record, so every result here is unambiguously
dated regardless of how wide the query range is.

NOTE on trimmed fields: raw Biostar records carry 20 fields, many of them
unreliable (absence, missingPunchOut - always false), unused/unpopulated
(lateIn, earlyOut, insufficientWorkTime - always "0:00:00"), duplicates
(normalOvertime == overtimeByTimeRate), or irrelevant to lateness (mealTime,
mileage, category, device names). Each report below returns only the fields
relevant to what it's reporting on.
"""

from biostar_connector import fetch_daily_attendance_range


def late_clock_in_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Late In" (confirmed spelling from real API data).
    Each record includes a "date" field showing which day it belongs to,
    and is trimmed down to only the fields relevant to lateness.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Late In" in r.get("exception", "")
    ]

    return {
        "exception_type": "Late Clock In",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }



def early_clock_out_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Early Out" (confirmed spelling from real API data).
    Each record includes a "date" field showing which day it belongs to,
    and is trimmed down to only the fields relevant to this report.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Early Out" in r.get("exception", "")
    ]

    return {
        "exception_type": "Early Clock Out",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }


def early_clock_in_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Early In".

    NOTE: UNVERIFIED SPELLING. We have not yet seen a real record with
    this exception in our data - this is built on the assumed symmetric
    naming pattern with "Late In" / "Early Out" / "Late Out". If this
    report comes back empty on a date range you know should have early
    arrivals, that's the signal this spelling is wrong. Find one real
    example and we'll correct the keyword here.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Early In" in r.get("exception", "")
    ]

    return {
        "exception_type": "Early Clock In",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }



def late_clock_out_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Late Out".

    NOTE: UNVERIFIED SPELLING. We have not yet seen a real record with
    this exception in our data - this is built on the assumed symmetric
    naming pattern with "Late In" / "Early Out" / "Early In". If this
    report comes back empty on a date range you know should have late
    departures, that's the signal this spelling is wrong. Find one real
    example and we'll correct the keyword here.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Late Out" in r.get("exception", "")
    ]

    return {
        "exception_type": "Late Clock Out",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }



def incomplete_attendance_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Missing Punch Out" (confirmed spelling from real API data).
    Each record includes a "date" field showing which day it belongs to,
    and is trimmed down to only the fields relevant to this report.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Missing Punch Out" in r.get("exception", "")
    ]

    return {
        "exception_type": "Incomplete Attendance",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }

def abscondment_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Absence" 
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Absence" in r.get("exception", "")
    ]

    return {
        "exception_type": "Abscondment",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }




def low_working_hours_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Insufficient work time" (confirmed spelling from real API data).
    Each record includes a "date" field showing which day it belongs to,
    and is trimmed down to only the fields relevant to this report.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Insufficient work time" in r.get("exception", "")
    ]

    return {
        "exception_type": "Low Working Hours",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }




def meal_punch_only_report(start_date, end_date, user_ids=None):
    """
    Returns all daily attendance records where the exception field
    contains "Meal Punch Only".

    NOTE: UNVERIFIED SPELLING. We have not yet seen a real record with
    this exception in our data - this is assumed to be a literal exception
    string from Biostar, same as "Late In", "Absence", etc. If this report
    comes back empty on a date range you know should have meal-only punches,
    that's the signal either the spelling is wrong or it needs a different
    substring. Find one real example and we'll correct the keyword here.
    """
    data = fetch_daily_attendance_range(start_date, end_date, user_ids)
    records = data.get("records", [])

    matched = [
        {
            "date": r.get("date"),
            "userId": r.get("userId"),
            "userName": r.get("userName"),
            "userGroupName": r.get("userGroupName"),
            "inTime": r.get("inTime"),
            "outTime": r.get("outTime"),
            "totalWorkTime": r.get("totalWorkTime"),
            "exception": r.get("exception"),
        }
        for r in records
        if "Meal Punch Only" in r.get("exception", "")
    ]

    return {
        "exception_type": "Meal Punch Only",
        "start_date": start_date,
        "end_date": end_date,
        "total": len(matched),
        "records": matched,
    }
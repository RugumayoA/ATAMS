"""
database.py - ATAMS local storage layer (SQLite)

Purpose:
    Stores processed daily attendance records fetched from the Biostar API
    so that historical reports are served instantly instead of re-calling
    the slow API. Biostar remains the live source of truth; this database
    is a permanent archive of past days.

Design rules:
    - One row per user per day, enforced by UNIQUE(userId, att_date).
    - Columns keep the EXACT Biostar API field names, so records can be
      inserted directly with no field mapping.
    - att_date is NOT in the API record; it comes from the query date and
      must be passed in explicitly.
    - fetched_days records which dates have been fully fetched, so an
      empty day (no punches) is distinguishable from a never-fetched day.
    - Only PAST days should ever be marked as fetched. Today is still
      accumulating punches and must always be fetched live.
"""

import sqlite3
import os
from datetime import datetime

# Database file lives next to this module, at the project root
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atams.db")

# The 20 fields exactly as returned by calldailyusers
API_FIELDS = [
    "userId",
    "userName",
    "userGroupName",
    "inTime",
    "outTime",
    "totalWorkTime",
    "normalOvertime",
    "overtimeByTimeRate",
    "exception",
    "absence",
    "insufficientWorkTime",
    "lateIn",
    "earlyOut",
    "missingPunchOut",
    "mealTime",
    "mealDeviceName",
    "inDeviceName",
    "outDeviceName",
    "mileage",
    "category",
]


def get_connection():
    """Open a connection with rows accessible by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they do not exist. Safe to call on every startup."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_attendance (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            att_date             TEXT NOT NULL,
            userId               TEXT NOT NULL,
            userName             TEXT,
            userGroupName        TEXT,
            inTime               TEXT,
            outTime              TEXT,
            totalWorkTime        TEXT,
            normalOvertime       TEXT,
            overtimeByTimeRate   TEXT,
            exception            TEXT,
            absence              INTEGER,
            insufficientWorkTime TEXT,
            lateIn               TEXT,
            earlyOut             TEXT,
            missingPunchOut      INTEGER,
            mealTime             TEXT,
            mealDeviceName       TEXT,
            inDeviceName         TEXT,
            outDeviceName        TEXT,
            mileage              TEXT,
            category             TEXT,
            fetched_at           TEXT NOT NULL,
            UNIQUE (userId, att_date)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fetched_days (
            att_date   TEXT PRIMARY KEY,
            fetched_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS public_holidays (
            holiday_date TEXT PRIMARY KEY,
            holiday_name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS directorates (
            department  TEXT PRIMARY KEY,
            directorate TEXT NOT NULL
        )
    """)

    # Speeds up date-range reads
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_attendance_date
        ON daily_attendance (att_date)
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Fetched-day tracking
# ---------------------------------------------------------------------------

def is_day_fetched(att_date):
    """Return True if this date has already been fully fetched and stored."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM fetched_days WHERE att_date = ?", (att_date,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def mark_day_fetched(att_date):
    """Record that a date has been fully fetched. Only call for PAST days."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO fetched_days (att_date, fetched_at) VALUES (?, ?)",
        (att_date, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Attendance storage and retrieval
# ---------------------------------------------------------------------------

def save_day(att_date, records):
    """
    Store all records for one date.

    att_date : "YYYY-MM-DD" string (the date used in the API query)
    records  : list of dicts exactly as returned by calldailyusers

    Uses INSERT OR REPLACE, so re-fetching a day safely overwrites it
    thanks to the UNIQUE(userId, att_date) constraint.
    """
    conn = get_connection()
    cur = conn.cursor()
    fetched_at = datetime.now().isoformat(timespec="seconds")

    columns = ["att_date"] + API_FIELDS + ["fetched_at"]
    placeholders = ", ".join(["?"] * len(columns))
    sql = "INSERT OR REPLACE INTO daily_attendance ({}) VALUES ({})".format(
        ", ".join(columns), placeholders
    )

    for record in records:
        values = [att_date]
        for field in API_FIELDS:
            value = record.get(field)
            # SQLite has no boolean type; store as 1/0
            if isinstance(value, bool):
                value = 1 if value else 0
            values.append(value)
        values.append(fetched_at)
        cur.execute(sql, values)

    conn.commit()
    conn.close()


def load_days(dates):
    """
    Load stored records for a list of "YYYY-MM-DD" dates.

    Returns a dict: { "YYYY-MM-DD": [record, record, ...], ... }
    Each record is a plain dict with the original API field names,
    plus "att_date". Booleans are restored from 1/0.
    Dates with no stored rows simply return an empty list.
    """
    results = {d: [] for d in dates}
    if not dates:
        return results

    conn = get_connection()
    cur = conn.cursor()
    placeholders = ", ".join(["?"] * len(dates))
    cur.execute(
        "SELECT * FROM daily_attendance WHERE att_date IN ({}) "
        "ORDER BY att_date, userName".format(placeholders),
        list(dates),
    )

    for row in cur.fetchall():
        record = dict(row)
        record.pop("id", None)
        record.pop("fetched_at", None)
        # Restore booleans
        record["absence"] = bool(record.get("absence"))
        record["missingPunchOut"] = bool(record.get("missingPunchOut"))
        results[record["att_date"]].append(record)

    conn.close()
    return results

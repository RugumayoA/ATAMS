import os
import time

import requests
import truststore
from dotenv import load_dotenv

# developer.caa.co.ug / api.caa.co.ug are internal gateways whose cert chain is
# trusted by Windows but isn't in the public certifi bundle requests uses by
# default. truststore makes requests verify against the OS trust store instead.
truststore.inject_into_ssl()

load_dotenv()

DAILY_CREDS = {
    "client_id": os.getenv("DAILY_CLIENT_ID"),
    "client_secret": os.getenv("DAILY_CLIENT_SECRET"),
}

ALL_USERS_CREDS = {
    "client_id": os.getenv("ALL_USERS_CLIENT_ID"),
    "client_secret": os.getenv("ALL_USERS_CLIENT_SECRET"),
}

TOKEN_URL = "https://developer.caa.co.ug/oauth2/token"

# stores tokens temporarily: { client_id: (token, expiry_time) }
_token_cache = {}

def get_token(creds):
    client_id = creds["client_id"]

    # check if we already have a valid token saved
    cached = _token_cache.get(client_id)
    if cached and time.time() < cached[1]:
        return cached[0]   # reuse existing token

    # otherwise, request a new one
    response = requests.post(
        TOKEN_URL,
        auth=(creds["client_id"], creds["client_secret"]),
        data={"grant_type": "client_credentials"},
    )
    response.raise_for_status()
    result = response.json()

    token = result["access_token"]
    expires_in = result.get("expires_in", 3600)

    # save it so we don't fetch it again until it's close to expiring
    _token_cache[client_id] = (token, time.time() + expires_in - 30)

    return token


DAILY_URL = "https://api.caa.co.ug/dailyattendanceapi/1.0.0/calldailyusers"
ALL_USERS_URL = "https://api.caa.co.ug/queryallemployeesfromatams/1.0.0/callallusers"


def fetch_daily_attendance(start_date, end_date, user_ids):
    token = get_token(DAILY_CREDS)

    # Biostar's API expects userID as ONE comma-separated string
    # (e.g. "01141, 01142, 01143"), not a JSON array. If the caller passes
    # a Python list (e.g. straight from a request body), convert it here
    # so callers don't have to worry about the format.
    if isinstance(user_ids, (list, tuple)):
        user_ids = ", ".join(str(uid) for uid in user_ids)

    response = requests.post(
        DAILY_URL,
        json={
            "attendancedaily": {
                "start_datetime": start_date,
                "end_datetime": end_date,
                "userID": user_ids,
            }
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    return response.json()


def fetch_all_users_attendance(start_date, end_date):
    token = get_token(ALL_USERS_CREDS)

    response = requests.post(
        ALL_USERS_URL,
        json={
            "attendance": {
                "start_datetime": start_date,
                "end_datetime": end_date,
            }
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    return response.json()


from datetime import datetime, timedelta

def fetch_daily_attendance_range(start_date, end_date, user_ids=None):
    """
    Loops day-by-day between start_date and end_date (inclusive), calling
    fetch_daily_attendance once per day, and manually attaches a "date"
    field to every record - because Biostar's API does NOT include a date
    field in its response, even across multi-day queries (confirmed
    against a real 423-record multi-day response with zero date fields).
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_records = []
    current = start
    while current <= end:
        day_str = current.strftime("%Y-%m-%d")
        data = fetch_daily_attendance(day_str, day_str, user_ids)
        for record in data.get("records", []):
            record["date"] = day_str
            all_records.append(record)
        current += timedelta(days=1)

    return {"records": all_records, "total": len(all_records)}
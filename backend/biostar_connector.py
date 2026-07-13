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


def _post_with_auth(url, creds, payload):
    # The gateway is WSO2-fronted; a token that was JUST issued can get a
    # spurious 401 for a moment because the gateway node hasn't synced with
    # the key manager yet (common right after a token cache miss, e.g. on
    # backend startup). Drop the cached token and retry once before giving up.
    token = get_token(creds)
    response = requests.post(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 401:
        _token_cache.pop(creds["client_id"], None)
        token = get_token(creds)
        response = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

    response.raise_for_status()
    return response.json()


def fetch_daily_attendance(start_date, end_date, user_ids):
    # Biostar's API expects userID as ONE comma-separated string
    # (e.g. "01141, 01142, 01143"), not a JSON array. If the caller passes
    # a Python list (e.g. straight from a request body), convert it here
    # so callers don't have to worry about the format.
    if isinstance(user_ids, (list, tuple)):
        user_ids = ", ".join(str(uid) for uid in user_ids)

    return _post_with_auth(
        DAILY_URL,
        DAILY_CREDS,
        {
            "attendancedaily": {
                "start_datetime": start_date,
                "end_datetime": end_date,
                "userID": user_ids,
            }
        },
    )


def fetch_all_users_attendance(start_date, end_date):
    return _post_with_auth(
        ALL_USERS_URL,
        ALL_USERS_CREDS,
        {
            "attendance": {
                "start_datetime": start_date,
                "end_datetime": end_date,
            }
        },
    )


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

from datetime import date, timedelta, timezone, datetime

from biostar_connector import search_events

# --- window helper (inline here just for the test) ---
EAT = timezone(timedelta(hours=3))

def eat_day_to_utc_window(day: date):
    start_eat = datetime(day.year, day.month, day.day, 0, 0, 0, tzinfo=EAT)
    end_eat   = datetime(day.year, day.month, day.day, 23, 59, 59, tzinfo=EAT)
    fmt = lambda dt: dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return fmt(start_eat), fmt(end_eat)

# --- the actual test ---
start, end = eat_day_to_utc_window(date(2026, 7, 21))
print(f"Querying device 939276804 for EAT 2026-07-21")
print(f"UTC window: {start} -> {end}")

body = {
    "Query": {
        "limit": 9999,
        "conditions": [
            {"column": "datetime", "operator": 3,
             "values": ["2026-07-21T00:00:00Z", "2026-07-21T23:00:00Z"]},
            {"column": "device_id", "operator": 2,
             "values": ["939276804", "939344349", "939754293", "939754211", "939344350"]},
            {"column": "user_group_id.id", "operator": 1, "values": ["0"]},
        ],
        "orders": [{"column": "datetime", "descending": False}],
    }
}

result = search_events(body)
rows = result["EventCollection"]["rows"]
print(f"Got {len(rows)} rows")

# ← this line is what's missing
person_rows = [r for r in rows if r.get("user_id", {}).get("user_id")]

print("First 10 people:")
for r in person_rows[:10]:
    u = r["user_id"]
    dev = r.get("device_id", {})
    code = r.get("event_type_id", {}).get("code", "?")
    print(f'  {r["datetime"]} | {u["user_id"]} | {u["name"]} | {dev.get("name","?")} | code {code}')
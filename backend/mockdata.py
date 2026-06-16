from datetime import datetime, timedelta
import random

# ── helpers ──────────────────────────────────────────────
def rand_time(hour, minute_range):
    return f"{hour:02d}:{random.randint(*minute_range):02d}"

# ── employees ────────────────────────────────────────────
employees = [
    {"user_id": "EMP001", "name": "Alice Nakato",     "department": "IT",          "directorate": "Technology",  "category": "Full Time",  "card_id": "CARD001", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2026-07-05"},
    {"user_id": "EMP002", "name": "Brian Mugisha",    "department": "HR",          "directorate": "Admin",       "category": "Full Time",  "card_id": "CARD002", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2026-12-01"},
    {"user_id": "EMP003", "name": "Carol Nambi",      "department": "Finance",     "directorate": "Finance",     "category": "Part Time",  "card_id": "CARD003", "card_status": "blacklisted", "has_credentials": True,  "is_new_user": False, "account_expiry": "2027-03-10"},
    {"user_id": "EMP004", "name": "David Okello",     "department": "IT",          "directorate": "Technology",  "category": "Full Time",  "card_id": "CARD004", "card_status": "active",      "has_credentials": False, "is_new_user": True,  "account_expiry": "2026-06-28"},
    {"user_id": "EMP005", "name": "Eva Namutebi",     "department": "HR",          "directorate": "Admin",       "category": "Contract",   "card_id": "CARD005", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2027-01-15"},
    {"user_id": "EMP006", "name": "Frank Ssebunya",   "department": "Security",    "directorate": "Operations",  "category": "Full Time",  "card_id": "CARD006", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2027-06-01"},
    {"user_id": "EMP007", "name": "Grace Akello",     "department": "Finance",     "directorate": "Finance",     "category": "Full Time",  "card_id": "CARD007", "card_status": "denied",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2026-09-20"},
    {"user_id": "EMP008", "name": "Henry Tumwine",    "department": "IT",          "directorate": "Technology",  "category": "Full Time",  "card_id": "CARD008", "card_status": "active",      "has_credentials": True,  "is_new_user": True,  "account_expiry": "2026-07-12"},
    {"user_id": "EMP009", "name": "Irene Zawedde",    "department": "HR",          "directorate": "Admin",       "category": "Part Time",  "card_id": "CARD009", "card_status": "active",      "has_credentials": False, "is_new_user": False, "account_expiry": "2027-05-30"},
    {"user_id": "EMP010", "name": "James Katende",    "department": "Security",    "directorate": "Operations",  "category": "Full Time",  "card_id": "CARD010", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2027-08-14"},
    {"user_id": "EMP011", "name": "Karen Naiga",      "department": "Finance",     "directorate": "Finance",     "category": "Contract",   "card_id": "CARD011", "card_status": "blacklisted", "has_credentials": True,  "is_new_user": False, "account_expiry": "2026-11-11"},
    {"user_id": "EMP012", "name": "Liam Byaruhanga",  "department": "IT",          "directorate": "Technology",  "category": "Full Time",  "card_id": "CARD012", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2027-02-28"},
    {"user_id": "EMP013", "name": "Mary Atuhaire",    "department": "HR",          "directorate": "Admin",       "category": "Full Time",  "card_id": "CARD013", "card_status": "active",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2027-04-19"},
    {"user_id": "EMP014", "name": "Noah Kiggundu",    "department": "Security",    "directorate": "Operations",  "category": "Full Time",  "card_id": "CARD014", "card_status": "denied",      "has_credentials": True,  "is_new_user": False, "account_expiry": "2026-08-08"},
    {"user_id": "EMP015", "name": "Olivia Nassuna",   "department": "Finance",     "directorate": "Finance",     "category": "Part Time",  "card_id": "CARD015", "card_status": "active",      "has_credentials": False, "is_new_user": True,  "account_expiry": "2026-07-25"},
]

# ── attendance derecords ────────────────────────────────────
attendance_records = [
    {"user_id": "EMP001", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:45", "check_out": "17:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP002", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:00", "check_out": "17:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP003", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": None,    "check_out": None,    "on_leave": True,  "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": False, "meal_accepted": False, "abscondment": False},
    {"user_id": "EMP004", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "09:30", "check_out": "17:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP005", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "07:45", "check_out": "16:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": False, "abscondment": False},
    {"user_id": "EMP006", "date": "2026-06-16", "shift": "Night",   "shift_start": "22:00", "shift_end": "06:00", "check_in": "22:00", "check_out": "06:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 2, "extra_hours": 1, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP007", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:00", "check_out": "12:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": True},
    {"user_id": "EMP008", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:10", "check_out": None,    "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP009", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": None,    "check_out": None,    "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": False, "meal_accepted": False, "abscondment": False},
    {"user_id": "EMP010", "date": "2026-06-16", "shift": "Night",   "shift_start": "22:00", "shift_end": "06:00", "check_in": "22:15", "check_out": "06:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 1, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP011", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:00", "check_out": "17:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP012", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "07:50", "check_out": "17:30", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 1, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP013", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:00", "check_out": "17:00", "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": True,  "meal_accepted": True,  "abscondment": False},
    {"user_id": "EMP014", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": None,    "check_out": None,    "on_leave": False, "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": False, "meal_accepted": False, "abscondment": False},
    {"user_id": "EMP015", "date": "2026-06-16", "shift": "Morning", "shift_start": "08:00", "shift_end": "17:00", "check_in": "08:00", "check_out": "17:00", "on_leave": True,  "is_weekend": False, "is_public_holiday": False, "overtime_hours": 0, "extra_hours": 0, "meal_punch": False, "meal_accepted": False, "abscondment": False},
]

# ── shift allocations ─────────────────────────────────────
shift_allocations = [
    {"user_id": "EMP001", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP002", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP003", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP004", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP005", "shift": "Morning", "schedule_template": "Flexible"},
    {"user_id": "EMP006", "shift": "Night",   "schedule_template": "Night Shift"},
    {"user_id": "EMP006", "shift": "Morning", "schedule_template": "Standard"},  # overlapping!
    {"user_id": "EMP007", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP008", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP009", "shift": "Morning", "schedule_template": "Flexible"},
    {"user_id": "EMP010", "shift": "Night",   "schedule_template": "Night Shift"},
    {"user_id": "EMP010", "shift": "Morning", "schedule_template": "Standard"},  # overlapping!
    {"user_id": "EMP011", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP012", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP013", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP014", "shift": "Morning", "schedule_template": "Standard"},
    {"user_id": "EMP015", "shift": "Morning", "schedule_template": "Flexible"},
]
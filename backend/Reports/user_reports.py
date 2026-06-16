from mockdata import employees
from datetime import datetime


def get_all_users():
    return employees

def get_new_users():
    return [e for e in employees if e["is_new_user"]]

def get_users_no_credentials():
    return [e for e in employees if not e["has_credentials"]]

def get_expiring_soon():
    today = datetime.today()
    return [
        e for e in employees
        if (datetime.strptime(e["account_expiry"], "%Y-%m-%d") - today).days <= 30
    ]

def get_users_by_category(category):
    return [e for e in employees if e["category"] == category]

def get_users_on_device():
    return [e for e in employees if e["card_status"] == "active"]

def get_exceptional_users():
    return [e for e in employees if e["card_status"] == "blacklisted"]
from mockdata import employees


def get_card_status():
    return [
        {
"user_id":     e["user_id"],
"name":        e["name"],
"card_id":     e["card_id"],
"card_status": e["card_status"]
        }
        for e in employees
    ]


def get_staff_assigned_to_cards():
    return [e for e in employees if e["card_id"]]


def get_blacklisted_cards():
    return [e for e in employees if e["card_status"] == "blacklisted"]


def get_denied_cards():
    return [e for e in employees if e["card_status"] == "denied"]


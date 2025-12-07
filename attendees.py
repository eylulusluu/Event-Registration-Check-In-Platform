import json
import uuid
import os

ATTENDEE_FILE = "data/attendees.json"

def ensure_file_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_attendees():
    ensure_file_exists(ATTENDEE_FILE)
    with open(ATTENDEE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_attendees(attendees):
    with open(ATTENDEE_FILE, "w", encoding="utf-8") as f:
        json.dump(attendees, f, indent=2, ensure_ascii=False)

def register_attendee(profile):
    attendees = load_attendees()

    required = ["first_name", "last_name", "email", "pin"]
    for r in required:
        if r not in profile:
            raise ValueError(f"Missing field: {r}")

    email = profile["email"].lower()
    if any(a["email"] == email for a in attendees):
        raise ValueError("Email already registered")

    attendee = {
        "id": str(uuid.uuid4()),
        "first_name": profile["first_name"],
        "last_name": profile["last_name"],
        "email": email,
        "organization": profile.get("organization", ""),
        "dietary": profile.get("dietary", ""),
        "ticket_type": profile.get("ticket_type", "general"),
        "pin": str(profile["pin"])
    }

    attendees.append(attendee)
    save_attendees(attendees)
    return attendee

def authenticate_attendee(email, pin):
    attendees = load_attendees()
    for a in attendees:
        if a["email"] == email.lower() and a["pin"] == str(pin):
            return a
    return None

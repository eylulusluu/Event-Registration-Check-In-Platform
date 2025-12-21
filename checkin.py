from datetime import datetime
import os


def check_in_attendee(registrations: list, registration_id: str) -> dict:
    reg = next((r for r in registrations if r["id"] == registration_id), None)
    if not reg:
        raise ValueError("Registration not found")

    if reg.get("cancelled"):
        raise ValueError("Registration is cancelled")

    if reg.get("status") != "confirmed":
        raise ValueError("Only confirmed attendees can check in")

    if reg.get("checked_in"):
        raise ValueError("Attendee already checked in")

    reg["checked_in"] = True
    reg["checkin_time"] = datetime.now().isoformat()

    return reg


def list_checked_in_attendees(registrations: list, event_id: str) -> list:
    return [
        r for r in registrations
        if r["event_id"] == event_id
        and r.get("checked_in")
        and not r.get("cancelled", False)
    ]


def generate_badge(attendee: dict, registration: dict, directory: str) -> str:
    os.makedirs(directory, exist_ok=True)

    filename = os.path.join(directory, f"badge_{registration['id']}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("EVENT BADGE\n")
        f.write("-----------------\n")
        f.write(f"Name: {attendee['name']}\n")
        f.write(f"Email: {attendee['email']}\n")
        f.write(f"Ticket Status: {registration['status']}\n")
        f.write(f"Confirmation Code: {registration['confirmation_code']}\n")
        f.write(f"Check-in Time: {registration.get('checkin_time', '-')}\n")

    return filename


def session_attendance(registrations: list, event_id: str, session_id: str) -> dict:
    count = sum(
        1 for r in registrations
        if r["event_id"] == event_id
        and r.get("checked_in")
        and session_id in r.get("sessions", [])
        and not r.get("cancelled", False)
    )

    return {
        "event_id": event_id,
        "session_id": session_id,
        "attendance": count
    }

from datetime import datetime
import os


def check_in_attendee(registrations: list, registration_id: str) -> dict:
    for reg in registrations:
        if reg["id"] == registration_id:
            if reg.get("checked_in"):
                raise ValueError("Attendee already checked in")

            reg["checked_in"] = True
            reg["checkin_time"] = datetime.now().isoformat()
            return reg

    raise ValueError("Registration not found")


def list_checked_in_attendees(registrations: list, event_id: str) -> list:
    return [
        r for r in registrations
        if r["event_id"] == event_id and r.get("checked_in")
    ]


def generate_badge(attendee: dict, registration: dict, directory: str) -> str:
    os.makedirs(directory, exist_ok=True)

    filename = f"{directory}/badge_{registration['id']}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("EVENT BADGE\n")
        f.write("-----------------\n")
        f.write(f"Name: {attendee['name']}\n")
        f.write(f"Email: {attendee['email']}\n")
        f.write(f"Ticket Type: {registration['ticket_type']}\n")
        f.write(f"Confirmation Code: {registration['id']}\n")

    return filename


def session_attendance(registrations: list, event_id: str, session_id: str) -> dict:
    count = 0
    for r in registrations:
        if (
            r["event_id"] == event_id
            and r.get("checked_in")
            and session_id in r.get("sessions", [])
        ):
            count += 1

    return {
        "event_id": event_id,
        "session_id": session_id,
        "attendance": count
    }

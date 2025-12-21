import uuid
from datetime import datetime


def create_registration(registrations: list, registration_data: dict, events: list) -> dict:
    event_id = registration_data["event_id"]
    attendee_id = registration_data["attendee_id"]
    payment_method = registration_data.get("payment_method", "cash")

    # Event kontrolü
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise ValueError("Event not found")

    capacity = event["capacity"]

    # Aktif (confirmed) kayıtlar
    confirmed_regs = [
        r for r in registrations
        if r["event_id"] == event_id
        and r.get("status") == "confirmed"
        and not r.get("cancelled", False)
    ]

    registration = {
        "id": str(uuid.uuid4()),
        "event_id": event_id,
        "attendee_id": attendee_id,
        "confirmation_code": str(uuid.uuid4())[:8],
        "payment_method": payment_method,
        "payment_status": "paid",
        "timestamp": datetime.now().isoformat(),
        "checked_in": False
    }

    # Capacity kontrolü
    if len(confirmed_regs) >= capacity:
        registration["status"] = "waitlist"
        registration["seat"] = None
    else:
        registration["status"] = "confirmed"
        registration["seat"] = len(confirmed_regs) + 1

    registrations.append(registration)
    return registration


def promote_waitlist(registrations: list, event_id: str) -> dict | None:
    # Aktif confirmed kayıtlar
    confirmed_regs = [
        r for r in registrations
        if r["event_id"] == event_id
        and r.get("status") == "confirmed"
        and not r.get("cancelled", False)
    ]

    # FIFO waitlist
    waitlisted = [
        r for r in registrations
        if r["event_id"] == event_id
        and r.get("status") == "waitlist"
        and not r.get("cancelled", False)
    ]

    if not waitlisted:
        return None

    promoted = waitlisted[0]
    promoted["status"] = "confirmed"
    promoted["seat"] = len(confirmed_regs) + 1

    return promoted


def cancel_registration(registrations: list, registration_id: str, events: list) -> dict:
    reg = next((r for r in registrations if r["id"] == registration_id), None)
    if not reg:
        raise ValueError("Registration not found")

    reg["cancelled"] = True

    promoted = promote_waitlist(registrations, reg["event_id"])

    return {
        "cancelled_registration": reg,
        "promoted_from_waitlist": promoted
    }


def calculate_event_revenue(registrations: list, event_id: str) -> float:
    return sum(
        r.get("price", 0)
        for r in registrations
        if r["event_id"] == event_id
        and r.get("status") == "confirmed"
        and r.get("payment_status") == "paid"
        and not r.get("cancelled", False)
    )


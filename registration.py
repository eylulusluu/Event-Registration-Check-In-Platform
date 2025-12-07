import uuid
from datetime import datetime

def create_registration(registrations: list, registration_data: dict, events: list) -> dict:
    event_id = registration_data["event_id"]
    attendee_id = registration_data["attendee_id"]
    payment_method = registration_data.get("payment_method", "cash")
    price = registration_data.get("price", 0)

    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise ValueError("Event not found")

    active_regs = [
        r for r in registrations
        if r["event_id"] == event_id and not r.get("waitlist") and not r.get("cancelled")
    ]

    capacity = event["capacity"]

    registration = {
        "id": str(uuid.uuid4()),
        "event_id": event_id,
        "attendee_id": attendee_id,
        "confirmation_code": str(uuid.uuid4())[:8],
        "payment_method": payment_method,
        "payment_status": "paid",
        "timestamp": datetime.now().isoformat(),
        "price": price
    }

    if len(active_regs) >= capacity:
        registration["waitlist"] = True
        registration["seat"] = None
    else:
        registration["waitlist"] = False
        registration["seat"] = len(active_regs) + 1

    registrations.append(registration)
    return registration


def promote_waitlist(registrations: list, event_id: str) -> dict | None:
    active_regs = [
        r for r in registrations
        if r["event_id"] == event_id and not r.get("waitlist") and not r.get("cancelled")
    ]

    waitlisted = [
        r for r in registrations
        if r["event_id"] == event_id and r.get("waitlist") and not r.get("cancelled")
    ]

    if not waitlisted:
        return None

    promoted = waitlisted[0]
    promoted["waitlist"] = False
    promoted["seat"] = len(active_regs) + 1

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

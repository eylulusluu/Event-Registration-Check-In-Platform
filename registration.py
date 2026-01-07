import uuid
from datetime import datetime

# PDF Source: [48, 49, 50, 51, 52, 53]

def create_registration(registrations: list, registration_data: dict, events: list) -> dict:
    event_id = registration_data["event_id"]
    attendee_id = registration_data["attendee_id"]
    
    # Event kontrolü
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        return {"error": "Etkinlik bulunamadı"}

    capacity = event["capacity"]
    
    # Aktif kayıt sayısını bul
    confirmed_count = sum(1 for r in registrations 
                          if r["event_id"] == event_id 
                          and r["status"] == "confirmed")

    reg_id = f"reg_{uuid.uuid4().hex[:8]}"
    
    registration = {
        "id": reg_id,
        "event_id": event_id,
        "attendee_id": attendee_id,
        "attendee_name": registration_data.get("attendee_name", ""),
        "confirmation_code": uuid.uuid4().hex[:6].upper(),
        "payment_status": "paid",
        "price": event.get("price", 0),
        "timestamp": datetime.now().isoformat(),
        "checked_in": False
    }

    if confirmed_count < capacity:
        registration["status"] = "confirmed"
    else:
        registration["status"] = "waitlist"
        registration["seat"] = None

    registrations.append(registration)
    return registration

def promote_waitlist(registrations: list, event_id: str):
    # Bekleme listesindeki ilk kişiyi bul
    waitlisted = next((r for r in registrations 
                       if r["event_id"] == event_id and r["status"] == "waitlist"), None)
    
    if waitlisted:
        waitlisted["status"] = "confirmed"
        return waitlisted
    return None

def cancel_registration(registrations: list, registration_id: str) -> dict:
    reg = next((r for r in registrations if r["id"] == registration_id), None)
    if not reg:
        return {"error": "Kayıt bulunamadı"}
    
    reg["status"] = "cancelled"
    
    # Bir kişi iptal ettiyse, yedekten birini al
    promoted = promote_waitlist(registrations, reg["event_id"])
    
    return {"cancelled": reg, "promoted": promoted}

def transfer_ticket(registrations: list, registration_id: str, new_attendee_id: str) -> dict:
    reg = next((r for r in registrations if r["id"] == registration_id), None)
    if not reg or reg["status"] == "cancelled":
        return {"error": "Transfer başarısız"}
    
    old_id = reg["attendee_id"]
    reg["attendee_id"] = new_attendee_id
    return {"status": "success", "old": old_id, "new": new_attendee_id}


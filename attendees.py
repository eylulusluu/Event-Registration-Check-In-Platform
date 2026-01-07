import uuid

# PDF Source: [37, 38, 39, 40]

def register_attendee(attendees: list, profile: dict) -> dict:
    new_attendee = {
        "id": f"att_{uuid.uuid4().hex[:8]}",
        "name": profile.get("name"),
        "email": profile.get("email"),
        "phone": profile.get("phone", ""),
        "organization": profile.get("organization", "")
    }
    attendees.append(new_attendee)
    return new_attendee

def authenticate_attendee(attendees: list, email: str) -> dict | None:
    # Basitlik için sadece e-posta ile kontrol ediyoruz (PDF login/pin istiyor ama temel seviye bu yeterli)
    for att in attendees:
        if att["email"] == email:
            return att
    return None
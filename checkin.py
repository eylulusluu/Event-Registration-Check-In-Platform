from datetime import datetime
import os

# PDF Source: [59, 60, 62]

def check_in_attendee(registrations: list, confirmation_code: str) -> dict:
    for reg in registrations:
        if reg.get("confirmation_code") == confirmation_code:
            if reg["status"] != "confirmed":
                return {"error": "Kayıt onaylı değil (Yedek liste veya İptal)"}
            
            if reg.get("checked_in"):
                return {"error": "Zaten giriş yapılmış!"}
            
            reg["checked_in"] = True
            reg["checkin_time"] = datetime.now().isoformat()
            return reg
            
    return {"error": "Kayıt kodu bulunamadı"}

def generate_badge(attendee_name: str, event_name: str, role: str = "Attendee"):
    # Basit bir metin dosyası rozet oluşturur
    badge_content = f"""
    *********************************
    * ETKİNLİK GİRİŞ KARTI     *
    *********************************
    * İSİM: {attendee_name}
    * ETKİNLİK: {event_name}
    * ROL: {role}
    *********************************
    """
    filename = f"badge_{attendee_name.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(badge_content)
    return filename

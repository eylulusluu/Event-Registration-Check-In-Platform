import uuid
from typing import List, Dict, Optional

# PDF Source: [28, 29, 30, 31, 32]

def _new_id(prefix: str = "evt") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_event(events: List[Dict], event_data: Dict) -> Dict:
    event = {
        "id": _new_id("evt"),
        "name": event_data.get("name", "İsimsiz Etkinlik"),
        "location": event_data.get("location", ""),
        "start_date": event_data.get("start_date", ""),
        "end_date": event_data.get("end_date", ""),
        "capacity": int(event_data.get("capacity", 0)),
        "price": float(event_data.get("price", 0.0)),
        "description": event_data.get("description", ""),
        "sessions": []
    }
    events.append(event)
    return event

def add_session(events: List[Dict], event_id: str, session_data: Dict) -> Optional[Dict]:
    for ev in events:
        if ev["id"] == event_id:
            session = {
                "id": _new_id("sess"),
                "title": session_data.get("title", ""),
                "speaker": session_data.get("speaker", ""),
                "start_time": session_data.get("start_time", ""),
                "end_time": session_data.get("end_time", ""),
                "room": session_data.get("room", ""),
                "capacity": int(session_data.get("capacity", 0))
            }
            ev["sessions"].append(session)
            return session
    return None

def list_sessions(events: List[Dict], event_id: str) -> List[Dict]:
    for ev in events:
        if ev["id"] == event_id:
            return ev.get("sessions", [])
    return []

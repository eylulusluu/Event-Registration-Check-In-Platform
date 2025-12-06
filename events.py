import json
import uuid
from typing import List, Dict, Optional

def _new_id(prefix: str = "evt") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def load_events(path: str) -> List[Dict]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_events(path: str, events: List[Dict]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(events, fh, ensure_ascii=False, indent=2)

def create_event(events: List[Dict], event_data: Dict) -> Dict:
    event = {
        "id": _new_id("evt"),
        "name": event_data.get("name", "Untitled Event"),
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

def update_event(events: List[Dict], event_id: str, updates: Dict) -> Optional[Dict]:
    for ev in events:
        if ev["id"] == event_id:
            ev.update(updates)
            if "capacity" in updates:
                ev["capacity"] = int(updates["capacity"])
            if "price" in updates:
                ev["price"] = float(updates["price"])
            return ev
    return None

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

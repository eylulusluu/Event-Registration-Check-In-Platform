import os
import json
import shutil
from datetime import datetime
from typing import Tuple, List, Dict

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def load_state(base_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    _ensure_dir(base_dir)

    def _load(p):
        try:
            with open(p, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    events = _load(os.path.join(base_dir, "events.json"))
    attendees = _load(os.path.join(base_dir, "attendees.json"))
    registrations = _load(os.path.join(base_dir, "registrations.json"))
    return events, attendees, registrations

def save_state(base_dir: str, events: List[Dict], attendees: List[Dict], registrations: List[Dict]) -> None:
    _ensure_dir(base_dir)

    with open(os.path.join(base_dir, "events.json"), "w", encoding="utf-8") as fh:
        json.dump(events, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(base_dir, "attendees.json"), "w", encoding="utf-8") as fh:
        json.dump(attendees, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(base_dir, "registrations.json"), "w", encoding="utf-8") as fh:
        json.dump(registrations, fh, ensure_ascii=False, indent=2)

def backup_state(base_dir: str, backup_dir: str):
    _ensure_dir(base_dir)
    _ensure_dir(backup_dir)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    backup_name = f"backup_{timestamp}"
    dest = os.path.join(backup_dir, backup_name)

    shutil.copytree(base_dir, dest)

    backed_files = []
    for root, _, files in os.walk(dest):
        for f in files:
            backed_files.append(os.path.join(root, f))

    return backed_files

import shutil
from datetime import datetime
import os


def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)

    copied_files = []

    for filename in os.listdir(base_dir):
        if filename.endswith(".json"):
            src = os.path.join(base_dir, filename)
            dst = os.path.join(backup_path, filename)
            shutil.copy(src, dst)
            copied_files.append(dst)

    return copied_files


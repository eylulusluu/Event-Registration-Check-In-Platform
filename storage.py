import json
import os
import shutil
from datetime import datetime

# PDF Source: [68, 69, 70, 71]

def load_data(path: str):
    """Verilen yoldaki JSON dosyasını okur."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(path: str, data: list):
    """Veriyi JSON formatında dosyaya yazar."""
    # Klasör yoksa oluştur
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def backup_state(base_dir: str = "data", backup_dir: str = "backups") -> list:
    """Tüm data klasörünü tarih damgası ile yedekler."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    
    try:
        shutil.copytree(base_dir, backup_path)
        return [backup_path]
    except Exception as e:
        print(f"Yedekleme hatası: {e}")
        return []


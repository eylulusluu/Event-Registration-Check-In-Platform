from events import load_events, save_events, create_event, add_session

DATA_DIR = "data"

def demo():
    events = load_events(f"{DATA_DIR}/events.json")
    print("Mevcut event sayısı:", len(events))

    ev = create_event(events, {
        "name": "Test Konferansı",
        "location": "İstanbul",
        "start_date": "2025-12-01",
        "end_date": "2025-12-02",
        "capacity": 200,
        "price": 50.0,
        "description": "Bu bir test etkinliğidir."
    })

    print("Oluşturulan event:", ev["id"])

    sess = add_session(events, ev["id"], {
        "title": "Açılış",
        "speaker": "Dr. A",
        "start_time": "2025-12-01T09:00",
        "end_time": "2025-12-01T09:30",
        "room": "Salon 1",
        "capacity": 100
    })

    print("Eklenen session:", sess["id"])

    save_events(f"{DATA_DIR}/events.json", events)
    print("Kayıt tamamlandı.")

if __name__ == "__main__":
    demo()

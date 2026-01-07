# PDF Source: [76, 77]

def generate_report(events: list, registrations: list):
    print("\n--- DETAYLI RAPOR ---")
    
    total_revenue = 0
    for ev in events:
        ev_regs = [r for r in registrations if r["event_id"] == ev["id"] and r["status"] == "confirmed"]
        revenue = sum(r.get("price", 0) for r in ev_regs)
        total_revenue += revenue
        
        checked_in = sum(1 for r in ev_regs if r.get("checked_in"))
        
        print(f"Etkinlik: {ev['name']}")
        print(f"  - Kayıtlı: {len(ev_regs)} / {ev['capacity']}")
        print(f"  - Giriş Yapan: {checked_in}")
        print(f"  - Gelir: {revenue} TL")
        print("-" * 20)
        
    print(f"TOPLAM PLATFORM GELİRİ: {total_revenue} TL")

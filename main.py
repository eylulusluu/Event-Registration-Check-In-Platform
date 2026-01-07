import sys
# events.py dosyasından gerekli fonksiyonları çekiyoruz
from events import load_events, save_events, create_event, add_session

DATA_DIR = "data"
EVENTS_FILE = f"{DATA_DIR}/events.json"

def print_menu():
    print("\n--- ETKİNLİK YÖNETİM SİSTEMİ ---")
    print("1. Etkinlikleri Listele")
    print("2. Yeni Etkinlik Oluştur (Create Event)")
    print("3. Çıkış")

def create_new_event_ui(events):
    print("\n--- Yeni Etkinlik Oluşturma ---")
    # Kullanıcıdan tek tek veri alıyoruz
    name = input("Etkinlik Adı: ")
    location = input("Konum: ")
    start_date = input("Başlangıç Tarihi (YYYY-MM-DD): ")
    end_date = input("Bitiş Tarihi (YYYY-MM-DD): ")
    
    # Sayısal değerler için hata kontrolü (Validation) [cite: 11]
    try:
        capacity = int(input("Kapasite (Sayı): "))
        price = float(input("Bilet Fiyatı: "))
    except ValueError:
        print("Hata: Kapasite ve Fiyat sayısal olmalıdır!")
        return

    description = input("Açıklama: ")

    # Toplanan verileri sözlük (dictionary) haline getiriyoruz
    new_event_data = {
        "name": name,
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "capacity": capacity,
        "price": price,
        "description": description
    }

    # events.py içindeki create_event fonksiyonunu çağırıyoruz
    created_event = create_event(events, new_event_data)
    print(f"\nBaşarılı! Yeni etkinlik oluşturuldu. ID: {created_event['id']}")
    
    # Değişikliği hemen kaydediyoruz [cite: 65]
    save_events(EVENTS_FILE, events)
    print("Veriler kaydedildi.")

def list_all_events(events):
    print("\n--- Mevcut Etkinlikler ---")
    if not events:
        print("Hiç etkinlik yok.")
    else:
        for ev in events:
            print(f"ID: {ev['id']} | Ad: {ev['name']} | Yer: {ev['location']}")

def main():
    # Program başlarken verileri yüklüyoruz
    events = load_events(EVENTS_FILE)
    
    while True:
        print_menu()
        secim = input("Seçiminiz (1-3): ")

        if secim == '1':
            list_all_events(events)
        elif secim == '2':
            create_new_event_ui(events)
        elif secim == '3':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()

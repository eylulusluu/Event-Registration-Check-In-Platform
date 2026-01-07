import sys
import storage
import events
import attendees
import registration
import checkin
import reports

# Veri Dosyalarının Yolları
DATA_DIR = "data"
EVENTS_FILE = f"{DATA_DIR}/events.json"
ATTENDEES_FILE = f"{DATA_DIR}/attendees.json"
REGS_FILE = f"{DATA_DIR}/registrations.json"

def main_menu():
    # Verileri Yükle
    event_list = storage.load_data(EVENTS_FILE)
    attendee_list = storage.load_data(ATTENDEES_FILE)
    reg_list = storage.load_data(REGS_FILE)

    while True:
        print("\n=== ETKİNLİK PLATFORMU ===")
        print("1. Organizatör Menüsü")
        print("2. Kayıt / Bilet Al (Katılımcı)")
        print("3. Personel / Check-In Menüsü")
        print("4. Raporlar")
        print("5. Yedekle ve Çıkış")
        
        choice = input("Seçiminiz: ")

        if choice == '1':
            organizer_menu(event_list)
            storage.save_data(EVENTS_FILE, event_list) # Her işlemden sonra kaydet

        elif choice == '2':
            attendee_menu(event_list, attendee_list, reg_list)
            storage.save_data(ATTENDEES_FILE, attendee_list)
            storage.save_data(REGS_FILE, reg_list)

        elif choice == '3':
            staff_menu(reg_list, event_list)
            storage.save_data(REGS_FILE, reg_list)

        elif choice == '4':
            reports.generate_report(event_list, reg_list)

        elif choice == '5':
            storage.save_data(EVENTS_FILE, event_list)
            storage.save_data(ATTENDEES_FILE, attendee_list)
            storage.save_data(REGS_FILE, reg_list)
            storage.backup_state()
            print("Veriler yedeklendi. Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim.")

def organizer_menu(event_list):
    print("\n--- Organizatör Paneli ---")
    print("1. Etkinlik Ekle")
    print("2. Etkinlikleri Listele")
    c = input("Seçim: ")
    if c == '1':
        name = input("Etkinlik Adı: ")
        cap = int(input("Kapasite: "))
        price = float(input("Fiyat: "))
        events.create_event(event_list, {"name": name, "capacity": cap, "price": price})
        print("Etkinlik oluşturuldu!")
    elif c == '2':
        for ev in event_list:
            print(f"[{ev['id']}] {ev['name']} (Kapasite: {ev['capacity']})")

def attendee_menu(event_list, attendee_list, reg_list):
    print("\n--- Bilet Alma Ekranı ---")
    # Önce Kullanıcı Oluştur veya Seç
    name = input("Adınız Soyadınız: ")
    email = input("Email Adresiniz: ")
    
    # Basitçe mevcut mu diye bakıyoruz, yoksa oluşturuyoruz
    user = attendees.authenticate_attendee(attendee_list, email)
    if not user:
        user = attendees.register_attendee(attendee_list, {"name": name, "email": email})
    
    print("\nMevcut Etkinlikler:")
    for ev in event_list:
        print(f"ID: {ev['id']} | {ev['name']} | {ev['price']} TL")
    
    ev_id = input("Katılmak istediğiniz Etkinlik ID'si: ")
    
    result = registration.create_registration(reg_list, {
        "event_id": ev_id,
        "attendee_id": user["id"],
        "attendee_name": user["name"]
    }, event_list)
    
    if "error" in result:
        print(f"HATA: {result['error']}")
    else:
        print(f"İşlem Başarılı! Durum: {result['status']}")
        print(f"Kayıt Kodunuz (Check-in için saklayın): {result['confirmation_code']}")

def staff_menu(reg_list, event_list):
    print("\n--- Personel Check-In ---")
    code = input("Katılımcı Kayıt Kodu (Confirmation Code): ")
    result = checkin.check_in_attendee(reg_list, code)
    
    if "error" in result:
        print(f"GİRİŞ REDDEDİLDİ: {result['error']}")
    else:
        print(f"GİRİŞ ONAYLANDI: {result['attendee_name']}")
        # Rozet bas
        ev_name = next((e['name'] for e in event_list if e['id'] == result['event_id']), "Etkinlik")
        file = checkin.generate_badge(result['attendee_name'], ev_name)
        print(f"Rozet oluşturuldu: {file}")

if __name__ == "__main__":
    main_menu()
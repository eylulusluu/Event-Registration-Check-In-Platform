import unittest
import sys
import os

# Ana dizindeki dosyalara erişmek için yol ayarı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Yeni yazdığımız modülleri çağırıyoruz
import events
import registration
import checkin

class TestEventSystem(unittest.TestCase):
    
    def setUp(self):
        # Her testten önce temiz liste oluşturuyoruz
        self.events_list = []
        self.registrations_list = []

    def test_full_flow(self):
        """Etkinlik oluşturma, Bilet alma ve Check-in akış testi"""
        
        # 1. Etkinlik Oluştur
        print("\nTEST 1: Etkinlik Oluşturuluyor...")
        event_data = {
            "name": "Test Event",
            "capacity": 2, # Kapasiteyi bilerek az verelim ki waitlist test edilsin
            "price": 100.0,
            "start_date": "2025-01-01"
        }
        new_event = events.create_event(self.events_list, event_data)
        self.assertEqual(len(self.events_list), 1)
        print(" -> Başarılı.")

        # 2. Normal Kayıt (Kapasite içi)
        print("TEST 2: Normal Kayıt Yapılıyor...")
        reg1 = registration.create_registration(self.registrations_list, {
            "event_id": new_event["id"],
            "attendee_id": "user1",
            "attendee_name": "Birinci Kisi"
        }, self.events_list)
        
        self.assertEqual(reg1["status"], "confirmed")
        print(" -> Başarılı (Status: Confirmed).")

        # 3. İkinci Kayıt (Kapasite Doldu)
        print("TEST 3: Kapasite Dolumu...")
        reg2 = registration.create_registration(self.registrations_list, {
            "event_id": new_event["id"],
            "attendee_id": "user2",
            "attendee_name": "Ikinci Kisi"
        }, self.events_list)
        self.assertEqual(reg2["status"], "confirmed") # Hala 2 kişi sınırındayız

        # 4. Waitlist Kaydı (3. Kişi)
        print("TEST 4: Waitlist (Yedek Liste) Kontrolü...")
        reg3 = registration.create_registration(self.registrations_list, {
            "event_id": new_event["id"],
            "attendee_id": "user3",
            "attendee_name": "Yedek Kisi"
        }, self.events_list)
        
        self.assertEqual(reg3["status"], "waitlist")
        self.assertIsNone(reg3["seat"])
        print(" -> Başarılı (Status: Waitlist).")

        # 5. Check-in İşlemi
        print("TEST 5: Check-in İşlemi...")
        code = reg1["confirmation_code"]
        check_result = checkin.check_in_attendee(self.registrations_list, code)
        self.assertTrue(check_result["checked_in"])
        print(" -> Başarılı (Giriş Yapıldı).")

if __name__ == '__main__':
    unittest.main()
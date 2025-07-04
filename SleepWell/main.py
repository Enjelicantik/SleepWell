
from models.user import User
from models.sleep_tracker import SleepTracker
from models.skin_health import SkinHealth
from models.reminder import Reminder
from datetime import datetime

# Inisialisasi objek
user = User("Enjeli")
sleep_tracker = SleepTracker()
skin_tracker = SkinHealth()
reminder = Reminder(user.ideal_sleep_hour)

def menu():
    while True:
        print("\n=== SleepWell Menu ===")
        print("1. Tambah catatan tidur")
        print("2. Tambah catatan kondisi kulit")
        print("3. Lihat semua catatan")
        print("4. Atur jam tidur ideal")
        print("5. Cek pengingat tidur")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == "1":
            jam_tidur = float(input("Masukkan durasi tidur (jam): "))
            skor = int(input("Skor kualitas tidur (1-10): "))
            sleep_tracker.log_entry({"durasi_tidur": jam_tidur, "skor_tidur": skor})
            print("✅ Catatan tidur disimpan!")

        elif pilihan == "2":
            kondisi = input("Kondisi kulit hari ini (berjerawat/kering/normal dll): ")
            skin_tracker.log_entry({"kondisi_kulit": kondisi})
            print("✅ Catatan kulit disimpan!")

        elif pilihan == "3":
            print("\n📊 Catatan Tidur:")
            for entry in sleep_tracker.view_entries():
                print(entry)
            print("\n💆 Catatan Kulit:")
            for entry in skin_tracker.view_entries():
                print(entry)

        elif pilihan == "4":
            jam = int(input("Masukkan jam tidur ideal (format 24 jam): "))
            user.set_sleep_goal(jam)
            reminder.ideal_hour = jam
            print(f"Jam tidur ideal diatur ke pukul {jam}:00")

        elif pilihan == "5":
            now = datetime.now().hour
            pesan = reminder.check_reminder(now)
            print(f"⏰ {pesan} (Sekarang pukul {now}:00)")

        elif pilihan == "6":
            print("Terima kasih telah menggunakan SleepWell!")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih 1-6.")

menu()

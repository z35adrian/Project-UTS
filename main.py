from datetime import datetime, date, timedelta
import csv
import os

# Nama file CSV penyimpanan
FILE_MEMBER = "data_member.csv"
FILE_ATTENDANCE = "attendance_log.csv"

# Data Akun untuk Simulasi Multi-Auth
users = {
    "admin@mail.com": {"password": "12345678", "role": "admin"},
    "staf@mail.com": {"password": "12345678", "role": "staff"},
    "kasir@mail.com": {"password": "12345678", "role": "kasir"}
}

def load_data_member():
    """Memuat semua data member dari file CSV."""
    data = []
    if os.path.exists(FILE_MEMBER):
        try:
            with open(FILE_MEMBER, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Gagal membaca file member: {e}")
    return data

def save_all_member(data_member):
    """Menulis ulang seluruh data member ke file CSV (digunakan untuk Update & Delete)."""
    try:
        with open(FILE_MEMBER, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["ID", "Nama", "Telepon", "Paket", "Expired"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for member in data_member:
                writer.writerow(member)
    except Exception as e:
        print(f"Gagal menyimpan data member: {e}")

def save_to_csv(member):
    """Menambahkan satu data member baru ke file CSV."""
    file_exists = os.path.exists(FILE_MEMBER)
    try:
        with open(FILE_MEMBER, mode="a", newline="", encoding="utf-8") as file:
            fieldnames = ["ID", "Nama", "Telepon", "Paket", "Expired"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            writer.writerow(member)
    except Exception as e:
        print(f"Gagal menyimpan ke file CSV: {e}")

def log_attendance(id_member, nama):
    """Mencatat riwayat check-in pengunjung oleh staff ke attendance_log.csv"""
    file_exists = os.path.exists(FILE_ATTENDANCE)
    waktu_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(FILE_ATTENDANCE, mode="a", newline="", encoding="utf-8") as file:
            fieldnames = ["ID", "Nama", "WaktuCheckIn"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({"ID": id_member, "Nama": nama, "WaktuCheckIn": waktu_checkin})
    except Exception as e:
        print(f"Gagal mencatat kehadiran: {e}")

def load_attendance():
    """Memuat seluruh data rekapitulasi kehadiran."""
    data = []
    if os.path.exists(FILE_ATTENDANCE):
        try:
            with open(FILE_ATTENDANCE, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Gagal membaca rekap kehadiran: {e}")
    return data

def login_system():
    print("=== SISTEM LOGIN CORNER GYM ===")
    email = input("Masukkan Email : ")
    password = input("Masukkan Password : ")

    if email in users and users[email]["password"] == password:
        role = users[email]["role"]
        print(f"\nLogin Berhasil! Selamat datang, {role.upper()}.")
        return role
    else:
        print("\nLogin Gagal! Email atau password salah.")
        return None

def daftar_member():
    print("\n=== PENDAFTARAN MEMBER CORNER GYM (KASIR) ===")
    data_member = load_data_member()

    nama = input("Nama member: ")
    telepon = input("Nomor telepon: ")

    print("\nPilihan Paket:")
    print("1. Harian")
    print("2. Bulanan")
    print("3. Couple")
    print("4. PT")

    pilihan = input("Pilih paket: ")

    if pilihan == "1":
        paket = "Harian"
        durasi = 1
    elif pilihan == "2":
        paket = "Bulanan"
        durasi = 30
    elif pilihan == "3":
        paket = "Couple"
        durasi = 30
    elif pilihan == "4":
        paket = "PT"
        durasi = 30
    else:
        print("Pilihan paket tidak tersedia!")
        return

    id_member = "GYM-" + str(len(data_member) + 1)
    mulai = date.today()
    expired = str(mulai + timedelta(days=durasi))

    member = {
        "ID": id_member,
        "Nama": nama,
        "Telepon": telepon,
        "Paket": paket,
        "Expired": expired
    }

    save_to_csv(member)

    print("\nPendaftaran Berhasil & Data Telah Disimpan!")
    print("ID Member:", id_member)
    print("Nama:", nama)
    print("Paket:", paket)
    print("Tanggal Expired:", expired)

def scan_member():
    """Fitur Staff untuk scan/cek ID Member & catat kehadiran"""
    print("\n=== SCAN / CEK MEMBER CORNER GYM (STAFF) ===")
    cari_id = input("Masukkan / Scan ID Member: ").strip().upper()
    
    data_member = load_data_member()
    found = False

    for member in data_member:
        if member["ID"] == cari_id:
            found = True
            nama = member["Nama"]
            paket = member["Paket"]
            tgl_expired_str = member["Expired"]
            
            tgl_expired = datetime.strptime(tgl_expired_str, "%Y-%m-%d").date()
            hari_ini = date.today()
            
            print("\n--- DETAIL MEMBER ---")
            print(f"ID Member      : {member['ID']}")
            print(f"Nama           : {nama}")
            print(f"Paket          : {paket}")
            print(f"No Telepon     : {member['Telepon']}")
            print(f"Tanggal Expired: {tgl_expired_str}")
            
            if hari_ini > tgl_expired:
                print("Status Member  : ❌ EXPIRED (Sudah Kadaluarsa) - Check-in ditolak.")
            else:
                sisa_hari = (tgl_expired - hari_ini).days
                print(f"Status Member  : ✅ AKTIF (Berlaku hingga {sisa_hari} hari lagi)")
                # Catat ke log kehadiran karena check-in berhasil
                log_attendance(member["ID"], nama)
                print("-> Check-in berhasil dicatat!")
            break

    if not found:
        print(f"\nMember dengan ID '{cari_id}' tidak ditemukan di database!")

def admin_dashboard():
    """Fitur Admin: CRUD Member & Rekapitulasi Kehadiran"""
    while True:
        print("\n=== DASHBOARD ADMIN CORNER GYM ===")
        print("1. Lihat Daftar Member")
        print("2. Tambah Member Baru")
        print("3. Edit Data Member")
        print("4. Hapus Member")
        print("5. Lihat Rekapitulasi Kehadiran Pengunjung")
        print("6. Keluar (Logout)")

        pilihan = input("Pilih menu admin (1-6): ")

        if pilihan == "1":
            data = load_data_member()
            print("\n--- DAFTAR SELURUH MEMBER ---")
            if not data:
                print("Belum ada data member.")
            else:
                for m in data:
                    print(f"ID: {m['ID']} | Nama: {m['Nama']} | Telp: {m['Telepon']} | Paket: {m['Paket']} | Expired: {m['Expired']}")

        elif pilihan == "2":
            daftar_member()

        elif pilihan == "3":
            data = load_data_member()
            cari_id = input("Masukkan ID Member yang ingin diedit: ").strip().upper()
            found = False
            for m in data:
                if m["ID"] == cari_id:
                    found = True
                    print(f"Data saat ini: Nama: {m['Nama']}, Telp: {m['Telepon']}, Paket: {m['Paket']}")
                    m["Nama"] = input("Nama baru (kosongkan jika tidak ingin ubah): ") or m["Nama"]
                    m["Telepon"] = input("No Telepon baru (kosongkan jika tidak ingin ubah): ") or m["Telepon"]
                    
                    ubah_paket = input("Ubah paket? (y/n): ").lower()
                    if ubah_paket == 'y':
                        p = input("Pilih paket baru (1. Harian, 2. Bulanan, 3. Couple, 4. PT): ")
                        durasi = 1 if p == "1" else 30
                        m["Paket"] = "Harian" if p == "1" else ("Bulanan" if p == "2" else ("Couple" if p == "3" else "PT"))
                        m["Expired"] = str(date.today() + timedelta(days=durasi))
                    
                    save_all_member(data)
                    print("\nData member berhasil diperbarui!")
                    break
            if not found:
                print("ID Member tidak ditemukan.")

        elif pilihan == "4":
            data = load_data_member()
            cari_id = input("Masukkan ID Member yang ingin dihapus: ").strip().upper()
            new_data = [m for m in data if m["ID"] != cari_id]
            
            if len(new_data) < len(data):
                save_all_member(new_data)
                print(f"\nMember dengan ID {cari_id} berhasil dihapus.")
            else:
                print("ID Member tidak ditemukan.")

        elif pilihan == "5":
            attendance = load_attendance()
            print("\n=== REKAPITULASI KEHADIRAN PENGUNJUNG ===")
            if not attendance:
                print("Belum ada data kehadiran (check-in) yang tercatat.")
            else:
                print(f"Total Keseluruhan Check-in: {len(attendance)} kali\n")
                
                # Hitung frekuensi check-in per ID Member
                rekap_hitung = {}
                for att in attendance:
                    key = (att["ID"], att["Nama"])
                    rekap_hitung[key] = rekap_hitung.get(key, 0) + 1
                
                print("--- Rangkuman Frekuensi Check-in per Member ---")
                for (mid, nama), count in rekap_hitung.items():
                    print(f"ID: {mid} | Nama: {nama} | Total Hadir: {count} kali")
                
                print("\n--- Riwayat Detail Check-in ---")
                for att in attendance:
                    print(f"[{att['WaktuCheckIn']}] ID: {att['ID']} - {att['Nama']}")

        elif pilihan == "6":
            print("Keluar dari dashboard admin.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def main():
    role = login_system()

    if role == "kasir":
        daftar_member()
    elif role == "staff":
        scan_member()
    elif role == "admin":
        admin_dashboard()

if __name__ == "__main__":
    main()
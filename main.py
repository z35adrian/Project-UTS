from datetime import date, timedelta

data_member = []

def daftar_member():
    print("\n=== PENDAFTARAN MEMBER CORNER GYM ===")

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

    # Membuat ID member otomatis
    id_member = "GYM-" + str(len(data_member) + 1)

    mulai = date.today()
    expired = mulai + timedelta(days=durasi)

    member = {
        "ID": id_member,
        "Nama": nama,
        "Telepon": telepon,
        "Paket": paket,
        "Expired": expired
    }

    data_member.append(member)

    print("\nPendaftaran Berhasil!")
    print("ID Member:", id_member)
    print("Nama:", nama)
    print("Paket:", paket)
    print("Tanggal Expired:", expired)


daftar_member()
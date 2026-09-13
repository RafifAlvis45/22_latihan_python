import matematika
import olahkata
import login_database


def tampilkan_menu_awal():
    print("\n===== SELAMAT DATANG =====")
    print("1. Login")
    print("2. Daftar Akun Baru")
    print("3. Keluar")


def tampilkan_menu():
    print("\n===== MENU =====")
    print("1. Cek Bilangan Prima")
    print("2. Cek Ganjil Genap")
    print("3. Mengubah Huruf jadi Besar (Capslock)")
    print("4. Keluar")


def main():
    # --- proses login/daftar akun dulu ---
    sudah_login = False
    while not sudah_login:
        tampilkan_menu_awal()
        pilih_awal = input("Pilih menu: ")

        if pilih_awal == "1":
            sudah_login = login_database.login()
        elif pilih_awal == "2":
            login_database.daftar_akun()
        elif pilih_awal == "3":
            print("Sampai jumpa!")
            return
        else:
            print("Pilihan tidak valid.")

    # --- setelah berhasil login, masuk ke menu utama ---
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            bil = matematika.minta_bilangan()
            matematika.BilPrima(bil)

        elif pilihan == "2":
            bil = matematika.minta_bilangan()
            matematika.GanjilGenap(bil)

        elif pilihan == "3":
            kata = input("Masukkan kata/kalimat: ")
            olahkata.Capslock(kata)

        elif pilihan == "4":
            lanjut = input("Yakin ingin keluar? (y/n): ")
            if lanjut.strip().lower() == "y":
                print("Program selesai. Sampai jumpa!")
                break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()

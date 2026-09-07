import matematika
import olahkata


def tampilkan_menu():
    print("\n===== MENU =====")
    print("1. Cek Bilangan Prima")
    print("2. Cek Ganjil Genap")
    print("3. Mengubah Huruf jadi Besar (Capslock)")
    print("4. Keluar")


def main():
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
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()

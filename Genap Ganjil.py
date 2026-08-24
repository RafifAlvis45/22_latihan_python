while True:
    angka = input("Masukkan angka (atau ketik 'close' untuk keluar): ")

    if angka.lower() == "close":
        print("Program dihentikan.")
        break

    if not angka.isdigit():
        print("Input tidak valid, masukkan angka atau 'close'.")
        continue

    angka = int(angka)

    if angka % 2 == 0:
        print(f"{angka} adalah bilangan genap.")
    else:
        print(f"{angka} adalah bilangan ganjil.")

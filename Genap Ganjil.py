def cek_input(teks):
    """Mengecek apakah input berupa angka atau perintah close"""
    return teks.lower() == "close" or teks.isdigit()


def tentukan_paritas(bil):
    """Menentukan apakah bilangan genap atau ganjil"""
    if bil % 2 == 0:
        print(f"{bil} adalah bilangan GENAP.")
    else:
        print(f"{bil} adalah bilangan GANJIL.")


def tentukan_prima(bil):
    """Menentukan apakah bilangan termasuk prima"""
    if bil <= 1:
        print(f"{bil} BUKAN bilangan prima.")
        return

    prima = True
    pembagi = 2

    while pembagi * pembagi <= bil:
        if bil % pembagi == 0:
            prima = False
            break
        pembagi += 1

    if prima:
        print(f"{bil} adalah bilangan PRIMA.")
    else:
        print(f"{bil} BUKAN bilangan prima.")


def minta_input():
    """Meminta input angka atau close"""
    while True:
        teks = input("Masukkan angka (atau ketik 'close' untuk keluar): ")

        if teks.lower() == "close":
            return None

        if cek_input(teks):
            return int(teks)

        print("Input tidak valid. Masukkan angka atau 'close'.")


def proses_angka(bil):
    """Menampilkan hasil pengecekan angka"""
    tentukan_paritas(bil)
    tentukan_prima(bil)


def main():
    while True:
        angka = minta_input()

        if angka is None:
            print("Program dihentikan.")
            break

        proses_angka(angka)


if __name__ == "__main__":
    main()

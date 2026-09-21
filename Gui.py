import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

# =========================================================
# PALET WARNA & FONT
# =========================================================
COLOR_BG = "#0f172a"          # navy gelap - background utama
COLOR_CARD = "#1e293b"        # panel/card sedikit lebih terang
COLOR_CARD_LIGHT = "#334155"  # border / hover card
COLOR_PRIMARY = "#6366f1"     # indigo - tombol utama
COLOR_PRIMARY_HOVER = "#818cf8"
COLOR_ACCENT = "#22d3ee"      # cyan - aksen / highlight
COLOR_SUCCESS = "#34d399"     # hijau
COLOR_DANGER = "#f87171"      # merah
COLOR_TEXT = "#f1f5f9"        # putih kebiruan
COLOR_TEXT_MUTED = "#94a3b8"  # abu-abu terang
COLOR_INPUT_BG = "#0b1220"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")
FONT_SECTION = ("Segoe UI", 12, "bold")


# =========================================================
# LOGIKA (pengganti sementara matematika.py & olahkata.py)
# =========================================================

def is_prima(bil: int) -> bool:
    if bil < 2:
        return False
    for i in range(2, int(bil ** 0.5) + 1):
        if bil % i == 0:
            return False
    return True


def is_ganjil_genap(bil: int) -> str:
    return "Genap" if bil % 2 == 0 else "Ganjil"


def capslock(kata: str) -> str:
    return kata.upper()


# =========================================================
# DATABASE SEDERHANA (pengganti sementara login_database.py)
# =========================================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def daftar_akun_db(username: str, password: str):
    if not username or not password:
        return False, "Username dan password tidak boleh kosong."
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "Akun berhasil dibuat. Silakan login."
    except sqlite3.IntegrityError:
        return False, "Username sudah terdaftar."
    finally:
        conn.close()


def login_db(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password))
    hasil = cur.fetchone()
    conn.close()
    return hasil is not None


# =========================================================
# WIDGET CUSTOM: Tombol dengan hover effect
# =========================================================

class RoundedButton(tk.Canvas):
    """Tombol custom dengan sudut membulat & efek hover, dibuat manual di Canvas."""

    def __init__(self, parent, text, command, bg=COLOR_PRIMARY, hover_bg=COLOR_PRIMARY_HOVER,
                 fg=COLOR_TEXT, width=180, height=42, radius=14, font=FONT_BUTTON):
        super().__init__(parent, width=width, height=height, bg=COLOR_CARD,
                          highlightthickness=0, bd=0)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.width = width
        self.height = height
        self.radius = radius

        self.shape = self._round_rect(2, 2, width - 2, height - 2, radius, fill=bg, outline="")
        self.label = self.create_text(width / 2, height / 2, text=text, fill=fg, font=font)

        for seq in ("<Button-1>", "<Enter>", "<Leave>"):
            self.tag_bind(self.shape, seq, self._on_event(seq))
            self.tag_bind(self.label, seq, self._on_event(seq))
            self.bind(seq, self._on_event(seq))

    def _on_event(self, seq):
        def handler(event):
            if seq == "<Enter>":
                self.itemconfig(self.shape, fill=self.hover_bg)
                self.configure(cursor="hand2")
            elif seq == "<Leave>":
                self.itemconfig(self.shape, fill=self.bg)
            elif seq == "<Button-1>":
                if self.command:
                    self.command()
        return handler

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


def styled_entry(parent, show=None, width=26):
    entry = tk.Entry(
        parent, show=show, width=width, font=FONT_LABEL,
        bg=COLOR_INPUT_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT,
        relief="flat", highlightthickness=1,
        highlightbackground=COLOR_CARD_LIGHT, highlightcolor=COLOR_ACCENT,
    )
    entry.configure(borderwidth=8)
    return entry


# =========================================================
# APLIKASI UTAMA
# =========================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Menu • Modern UI")
        self.geometry("460x560")
        self.resizable(False, False)
        self.configure(bg=COLOR_BG)
        self._center_window()

        self.username_login = None

        self.container = tk.Frame(self, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True)

        self.show_login_frame()

    def _center_window(self):
        self.update_idletasks()
        w, h = 460, 560
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def make_card(self, parent, **pack_opts):
        card = tk.Frame(parent, bg=COLOR_CARD, highlightbackground=COLOR_CARD_LIGHT,
                         highlightthickness=1, bd=0)
        card.pack(**pack_opts)
        return card

    # ---------------- FRAME: LOGIN / DAFTAR ----------------
    def show_login_frame(self):
        self.clear_container()
        frame = self.container

        # Header dengan aksen warna
        header = tk.Frame(frame, bg=COLOR_BG)
        header.pack(fill="x", pady=(45, 10))

        tk.Label(header, text="✦", font=("Segoe UI", 26), fg=COLOR_ACCENT, bg=COLOR_BG).pack()
        tk.Label(header, text="SELAMAT DATANG", font=FONT_TITLE, fg=COLOR_TEXT, bg=COLOR_BG).pack(pady=(6, 0))
        tk.Label(header, text="Masuk atau buat akun untuk melanjutkan",
                 font=FONT_SUBTITLE, fg=COLOR_TEXT_MUTED, bg=COLOR_BG).pack(pady=(2, 0))

        card = self.make_card(frame, pady=20, padx=30, fill="x")
        inner = tk.Frame(card, bg=COLOR_CARD)
        inner.pack(padx=25, pady=25, fill="x")

        tk.Label(inner, text="Username", font=FONT_LABEL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD,
                 anchor="w").pack(fill="x", pady=(0, 4))
        entry_user = styled_entry(inner)
        entry_user.pack(fill="x", pady=(0, 14), ipady=6)

        tk.Label(inner, text="Password", font=FONT_LABEL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD,
                 anchor="w").pack(fill="x", pady=(0, 4))
        entry_pass = styled_entry(inner, show="•")
        entry_pass.pack(fill="x", pady=(0, 20), ipady=6)

        def do_login():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            if login_db(username, password):
                self.username_login = username
                self.show_menu_frame()
            else:
                messagebox.showerror("Gagal", "Username atau password salah.")

        def do_daftar():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            ok, pesan = daftar_akun_db(username, password)
            (messagebox.showinfo if ok else messagebox.showerror)(
                "Sukses" if ok else "Gagal", pesan
            )

        btn_row = tk.Frame(inner, bg=COLOR_CARD)
        btn_row.pack(fill="x")

        RoundedButton(btn_row, "Masuk", do_login, bg=COLOR_PRIMARY,
                      hover_bg=COLOR_PRIMARY_HOVER, width=175, height=42).pack(side="left")
        RoundedButton(btn_row, "Daftar Akun", do_daftar, bg=COLOR_CARD_LIGHT,
                      hover_bg="#475569", width=175, height=42).pack(side="right")

        tk.Label(frame, text="keluar aplikasi", font=("Segoe UI", 9, "underline"),
                 fg=COLOR_TEXT_MUTED, bg=COLOR_BG, cursor="hand2").pack(pady=18)
        frame.winfo_children()[-1].bind("<Button-1>", lambda e: self.destroy())

    # ---------------- FRAME: MENU UTAMA ----------------
    def show_menu_frame(self):
        self.clear_container()
        frame = self.container

        header = tk.Frame(frame, bg=COLOR_BG)
        header.pack(fill="x", pady=(30, 15), padx=25)

        left = tk.Frame(header, bg=COLOR_BG)
        left.pack(side="left")
        tk.Label(left, text=f"Halo, {self.username_login} 👋", font=FONT_SECTION,
                 fg=COLOR_TEXT, bg=COLOR_BG, anchor="w").pack(anchor="w")
        tk.Label(left, text="Pilih salah satu fitur di bawah",
                 font=FONT_LABEL, fg=COLOR_TEXT_MUTED, bg=COLOR_BG, anchor="w").pack(anchor="w")

        def logout():
            self.username_login = None
            self.show_login_frame()

        RoundedButton(header, "Logout", logout, bg=COLOR_DANGER, hover_bg="#fb7185",
                      width=90, height=34, font=("Segoe UI", 9, "bold")).pack(side="right")

        # --- Card: Cek Bilangan ---
        card1 = self.make_card(frame, fill="x", padx=25, pady=(5, 12))
        c1_inner = tk.Frame(card1, bg=COLOR_CARD)
        c1_inner.pack(fill="x", padx=20, pady=18)

        tk.Label(c1_inner, text="🔢  Cek Bilangan", font=FONT_SECTION,
                 fg=COLOR_TEXT, bg=COLOR_CARD, anchor="w").pack(anchor="w", pady=(0, 10))

        entry_bil = styled_entry(c1_inner, width=15)
        entry_bil.pack(side="left", ipady=6, padx=(0, 10))

        def cek_prima():
            try:
                bil = int(entry_bil.get())
            except ValueError:
                messagebox.showerror("Error", "Masukkan angka yang valid.")
                return
            hasil = "PRIMA ✅" if is_prima(bil) else "BUKAN PRIMA ❌"
            messagebox.showinfo("Hasil", f"{bil} adalah {hasil}")

        def cek_ganjil_genap():
            try:
                bil = int(entry_bil.get())
            except ValueError:
                messagebox.showerror("Error", "Masukkan angka yang valid.")
                return
            messagebox.showinfo("Hasil", f"{bil} adalah {is_ganjil_genap(bil)}")

        btns1 = tk.Frame(c1_inner, bg=COLOR_CARD)
        btns1.pack(side="left")
        RoundedButton(btns1, "Cek Prima", cek_prima, bg=COLOR_PRIMARY,
                      hover_bg=COLOR_PRIMARY_HOVER, width=110, height=38).pack(side="left", padx=(0, 8))
        RoundedButton(btns1, "Ganjil/Genap", cek_ganjil_genap, bg=COLOR_ACCENT,
                      hover_bg="#67e8f9", fg="#0f172a", width=120, height=38).pack(side="left")

        # --- Card: Capslock ---
        card2 = self.make_card(frame, fill="x", padx=25, pady=(0, 12))
        c2_inner = tk.Frame(card2, bg=COLOR_CARD)
        c2_inner.pack(fill="x", padx=20, pady=18)

        tk.Label(c2_inner, text="🔠  Ubah Huruf jadi Besar", font=FONT_SECTION,
                 fg=COLOR_TEXT, bg=COLOR_CARD, anchor="w").pack(anchor="w", pady=(0, 10))

        row2 = tk.Frame(c2_inner, bg=COLOR_CARD)
        row2.pack(fill="x")

        entry_kata = styled_entry(row2, width=20)
        entry_kata.pack(side="left", ipady=6, padx=(0, 10))

        def do_capslock():
            kata = entry_kata.get()
            if not kata:
                messagebox.showerror("Error", "Masukkan kata/kalimat.")
                return
            messagebox.showinfo("Hasil", capslock(kata))

        RoundedButton(row2, "Ubah", do_capslock, bg=COLOR_SUCCESS, hover_bg="#6ee7b7",
                      fg="#0f172a", width=100, height=38).pack(side="left")

        # --- Footer ---
        footer = tk.Frame(frame, bg=COLOR_BG)
        footer.pack(fill="x", pady=(10, 0), padx=25)
        tk.Label(footer, text="keluar aplikasi", font=("Segoe UI", 9, "underline"),
                 fg=COLOR_TEXT_MUTED, bg=COLOR_BG, cursor="hand2").pack(anchor="center")
        footer.winfo_children()[-1].bind("<Button-1>", lambda e: self.destroy())


if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()

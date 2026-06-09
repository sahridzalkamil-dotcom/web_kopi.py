import sqlite3
import streamlit as st

# === 1. PENGATURAN DATABASE ===
def koneksi_db():
    koneksi = sqlite3.connect("kopi_baru.db")
    return koneksi

# Membuat tabel jika belum ada saat web pertama dibuka
conn = koneksi_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kopi TEXT NOT NULL,
    harga INTEGER NOT NULL
)
""")
conn.commit()
conn.close()

# === 2. TAMPILAN UTAMA WEB (STREAMLIT) ===
st.set_page_config(page_title="FOR REST COFFEE", page_icon="☕", layout="centered")

st.title("☕ FOR REST COFFEE")
st.subheader("Sistem Manajemen Menu Cafe")
st.write("Selamat datang! Kelola daftar menu kopi kamu secara langsung di sini.")
st.markdown("---")

# === 3. FORM INPUT MENU BARU ===
st.header("➕ Tambah Menu Baru")
nama_kopi = st.text_input("Nama Kopi Baru", placeholder="Misal: Palm Sugar Latte")
harga_input = st.text_input("Harga (Rp)", placeholder="Misal: 25.000")

if st.button("Simpan Menu", type="primary"):
    if nama_kopi and harga_input:
        harga_bersih = harga_input.replace(".", "")
        try:
            harga_angka = int(harga_bersih)
            conn = koneksi_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO menu (nama_kopi, harga) VALUES (?, ?)", (nama_kopi, harga_angka))
            conn.commit()
            conn.close()
            st.success(f"🎉 Sukses! Menu '{nama_kopi}' berhasil disimpan ke database.")
        except ValueError:
            st.error("❌ Waduh, input harga harus berupa angka ya!")
    else:
        st.warning("⚠️ Mohon isi nama menu dan harganya terlebih dahulu.")

st.markdown("---")

# === 4. TAMPILAN DAFTAR MENU ===
st.header("📋 Daftar Menu Saat Ini")
conn = koneksi_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM menu ORDER BY id ASC")
semua_menu = cursor.fetchall()
conn.close()

if semua_menu:
    for baris in semua_menu:
        st.info(f"**ID: {baris[0]}** | ☕ **{baris[1]}** | 💵 Harga: Rp {baris[2]:,}".replace(",", "."))
else:
    st.write("*Belum ada menu yang tersimpan di database.*")

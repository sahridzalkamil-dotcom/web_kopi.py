import sqlite3
import streamlit as st
import pandas as pd # Tambahan untuk mengolah data grafik

# === 1. PENGATURAN DATABASE ===
def koneksi_db():
    koneksi = sqlite3.connect("for_rest_coffee.db")
    return koneksi

# Membuat tabel menu & transaksi jika belum ada
conn = koneksi_db()
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nama_kopi TEXT, harga INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS transaksi (id INTEGER PRIMARY KEY AUTOINCREMENT, nama_kopi TEXT, jumlah INTEGER, total_harga INTEGER, tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
conn.commit()
conn.close()

# === 2. TAMPILAN UTAMA ===
st.set_page_config(page_title="FOR REST COFFEE PRO", page_icon="📊", layout="centered")

st.title("☕ FOR REST COFFEE PRO")
st.subheader("Sistem Manajemen & Analisis Penjualan")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Menu", "➕ Tambah", "💰 Kasir", "📊 Dashboard"])

# Ambil data menu untuk digunakan di semua tab
conn = koneksi_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM menu")
semua_menu = cursor.fetchall()
conn.close()

# ==========================================
# TAB 1: DAFTAR & HAPUS MENU
# ==========================================
with tab1:
    st.header("📋 Daftar Menu")
    if semua_menu:
        for baris in semua_menu:
            kol1, kol2 = st.columns([4, 1])
            kol1.info(f"**{baris[1]}** - Rp {baris[2]:,}".replace(",", "."))
            if kol2.button("Hapus", key=f"hps_{baris[0]}"):
                conn = koneksi_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM menu WHERE id = ?", (baris[0],))
                conn.commit()
                conn.close()
                st.rerun()
    else:
        st.write("Menu kosong.")

# ==========================================
# TAB 2: TAMBAH MENU
# ==========================================
with tab2:
    st.header("➕ Tambah Menu")
    n_kopi = st.text_input("Nama Kopi")
    h_kopi = st.number_input("Harga", min_value=0, step=500)
    if st.button("Simpan Menu"):
        conn = koneksi_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu (nama_kopi, harga) VALUES (?, ?)", (n_kopi, h_kopi))
        conn.commit()
        conn.close()
        st.success("Menu tersimpan!")
        st.rerun()

# ==========================================
# TAB 3: KASIR & SIMPAN TRANSAKSI
# ==========================================
with tab3:
    st.header("💰 Kasir")
    if semua_menu:
        opsi_kopi = {b[1]: b[2] for b in semua_menu}
        pilih = st.selectbox("Pilih Menu", list(opsi_kopi.keys()))
        qty = st.number_input("Jumlah Gelas", min_value=1, value=1)
        total = opsi_kopi[pilih] * qty
        
        st.write(f"### Total: Rp {total:,}".replace(",", "."))
        
        if st.button("Selesaikan & Simpan Transaksi", type="primary"):
            conn = koneksi_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transaksi (nama_kopi, jumlah, total_harga) VALUES (?, ?, ?)", (pilih, qty, total))
            conn.commit()
            conn.close()
            st.success(f"Berhasil! Transaksi {pilih} tercatat.")
    else:
        st.warning("Tambahkan menu dulu!")

# ==========================================
# TAB 4: DASHBOARD & GRAFIK (DATA SCIENCE)
# ==========================================
with tab4:
    st.header("📊 Analisis Penjualan")
    
    # Ambil data transaksi
    conn = koneksi_db()
    df = pd.read_sql_query("SELECT nama_kopi, jumlah, total_harga FROM transaksi", conn)
    conn.close()

    if not df.empty:
        # --- Ringkasan Angka ---
        total_pendapatan = df['total_harga'].sum()
        total_terjual = df['jumlah'].sum()
        
        c1, c2 = st.columns(2)
        c1.metric("Total Pendapatan", f"Rp {total_pendapatan:,}".replace(",", "."))
        c2.metric("Total Gelas Terjual", f"{total_terjual} Gelas")

        st.markdown("---")
        
        # --- Visualisasi Grafik Bar ---
        st.subheader("📈 Produk Paling Laris (Gelas)")
        # Mengelompokkan data berdasarkan nama kopi
        data_grafik = df.groupby('nama_kopi')['jumlah'].sum().sort_values(ascending=False)
        st.bar_chart(data_grafik)

        st.subheader("📋 Riwayat Transaksi Terakhir")
        st.dataframe(df.tail(5), use_container_width=True) # Menampilkan tabel data 5 terakhir
    else:
        st.write("Belum ada data transaksi untuk dianalisis.")

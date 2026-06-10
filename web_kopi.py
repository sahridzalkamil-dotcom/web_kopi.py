import sqlite3
import streamlit as st

# === 1. PENGATURAN DATABASE ===
def koneksi_db():
    koneksi = sqlite3.connect("for_rest_coffee.db")
    return koneksi

# Membuat tabel menu jika belum ada
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
st.subheader("Sistem Manajemen & Kasir Cafe")
st.write("Kelola menu, lihat galeri produk, dan lakukan simulasi transaksi kasir.")

# Navigasi Tab: Dashboard dihapus, diganti dengan Tab Galeri Foto Menu
tab1, tab2, tab3, tab4 = st.tabs(["📋 Daftar & Hapus Menu", "➕ Tambah Menu", "💰 Simulasi Kasir", "🖼️ Galeri Foto Menu"])

# ==========================================
# TAB 1: DAFTAR MENU & FITUR HAPUS
# ==========================================
with tab1:
    st.header("📋 Daftar Menu Saat Ini")
    
    conn = koneksi_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu ORDER BY id ASC")
    semua_menu = cursor.fetchall()
    conn.close()

    if semua_menu:
        for baris in semua_menu:
            id_menu = baris[0]
            nama_menu = baris[1]
            harga_menu = baris[2]
            
            kolom_info, kolom_tombol = st.columns([4, 1])
            
            with kolom_info:
                st.info(f"**ID: {id_menu}** | ☕ **{nama_menu}** | 💵 Rp {harga_menu:,}".replace(",", "."))
            
            with kolom_tombol:
                if st.button("Hapus", key=f"hapus_{id_menu}", type="secondary"):
                    conn = koneksi_db()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM menu WHERE id = ?", (id_menu,))
                    conn.commit()
                    conn.close()
                    st.toast(f"🗑️ Menu '{nama_menu}' berhasil dihapus!")
                    st.rerun()
    else:
        st.write("*Belum ada menu yang tersimpan di database FOR REST COFFEE.*")

# ==========================================
# TAB 2: TAMBAH MENU BARU
# ==========================================
with tab2:
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
                
                st.success(f"🎉 Sukses! Menu '{nama_kopi}' berhasil disimpan.")
                st.rerun()
            except ValueError:
                st.error("❌ Input harga harus berupa angka!")
        else:
            st.warning("⚠️ Mohon isi nama menu dan harganya.")

# ==========================================
# TAB 3: SIMULASI KASIR (KEMBALI KE NOTA MURNI)
# ==========================================
with tab3:
    st.header("💰 Simulasi Hitung Transaksi")
    
    if semua_menu:
        pilihan_kopi = {baris[1]: baris[2] for baris in semua_menu} 
        kopi_terpilih = st.selectbox("Pilih Kopi yang Dibeli", list(pilihan_kopi.keys()))
        jumlah_beli = st.number_input("Jumlah Porsi/Gelas", min_value=1, step=1, value=1)
        
        harga_satuan = pilihan_kopi[kopi_terpilih]
        total_bayar = harga_satuan * jumlah_beli
        
        st.markdown("### 📄 Struk Nota Digital")
        st.code(f"""
====================================
          FOR REST COFFEE           
====================================
 Menu   : {kopi_terpilih}
 Harga  : Rp {harga_satuan:,} x {jumlah_beli}
------------------------------------
 TOTAL  : Rp {total_bayar:,}
====================================
        Terima Kasih & Selamat
             Beristirahat!
        """.replace(",", "."), language="text")
        
    else:
        st.write("*Belum bisa melakukan transaksi karena belum ada menu di database.*")

# ==========================================
# TAB 4: VISUALISASI GALERI FOTO MENU (BARU!)
# ==========================================
with tab4:
    st.header("🖼️ Galeri Visual Menu Kopi")
    st.write("Tampilan visual estetik menu andalan FOR REST COFFEE untuk memanjakan mata pelanggan.")
    
    # Membuat susunan grid/kolom untuk gambar
    kolom1, kolom2 = st.columns(2)
    
    with kolom1:
        st.image("https://images.unsplash.com/photo-1541167760496-1628856ab772?w=500", 
                 caption="☕ Espresso & Kopi Susu Klasik", use_container_width=True)
        st.caption("*Perpaduan espresso mantap dengan susu lembut, cocok ditemani waktu santai.*")
        
    with kolom2:
        st.image("https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500", 
                 caption="🧊 Iced Latte Premium", use_container_width=True)
        st.caption("*Kesegaran es kopi latte premium untuk mendinginkan hari yang sibuk.*")
        
    st.markdown("---")
    st.info("💡 **Tips:** Gambar di atas menggunakan URL gambar langsung. Di masa depan, kita bisa kembangkan agar gambarnya bisa otomatis berubah sesuai menu yang kamu input!")

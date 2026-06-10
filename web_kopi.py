import sqlite3
import streamlit as st

# === 1. PENGATURAN DATABASE ===
def koneksi_db():
    koneksi = sqlite3.connect("for_rest_coffee.db")
    return koneksi

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

# === 2. TAMPILAN UTAMA & CUSTOM CSS ===
st.set_page_config(page_title="FOR REST COFFEE", page_icon="☕", layout="centered")

# Menyuntikkan CSS Kustom untuk mengubah tampilan bawaan Streamlit
st.markdown("""
<style>
    /* Mengubah font utama dan latar belakang aplikasi */
    .stApp {
        background-color: #fcf8f2;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Mempercantik Judul Utama */
    h1 {
        color: #4a2c11 !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Mempercantik kotak Info Menu (Tab 1) */
    .stAlert {
        background-color: #ffffff !important;
        border-left: 5px solid #8B5A2B !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Kustomisasi Tombol Hapus (Merah Estetik) */
    div.stButton > button {
        background-color: #e63946 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #d62828 !important;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(230,57,70,0.3);
    }
    
    /* Kustomisasi Tombol Simpan (Cokelat Kopi) */
    div.stButton > button[type="primary"] {
        background-color: #6f4e37 !important;
        color: white !important;
        border-radius: 6px !important;
    }
    div.stButton > button[type="primary"]:hover {
        background-color: #4a2c11 !important;
    }
</style>
""", unsafe_allow_html=True)


# === 3. SENTUHAN JAVASCRIPT & HTML (Greeting Dinamis) ===
# Memasukkan skrip JS untuk menyapa pengguna berdasarkan jam di device mereka
st.components.v1.html("""
<div id="greeting-box" style="
    padding: 15px; 
    background: linear-gradient(135deg, #8B5A2B, #6f4e37); 
    color: white; 
    border-radius: 10px; 
    text-align: center; 
    font-family: 'Segoe UI', sans-serif;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    margin-bottom: 10px;
">
    <span id="greeting-text">Selamat Datang!</span>
</div>

<script>
    const jam = new Date().getHours();
    let sapaan = "Selamat Istirahat di FOR REST COFFEE! ☕";
    
    if (jam >= 5 && jam < 11) {
        sapaan = "🌅 Selamat Pagi! Semangat beraktivitas ditemani FOR REST COFFEE!";
    } else if (jam >= 11 && jam < 15) {
        sapaan = "☀️ Selamat Siang! Waktunya break & 'For Rest' sejenak dengan kopi dingin!";
    } else if (jam >= 15 && jam < 18) {
        sapaan = "🌆 Selamat Sore! Nikmati senja syahdu bersama hangatnya cita rasa kami!";
    } else {
        sapaan = "🌙 Selamat Malam! Waktunya rileks dan santai menikmati suasana malam.";
    }
    
    document.getElementById("greeting-text").innerText = sapaan;
</script>
""", height=75)


# === 4. LOGIKA NAVIGASI STREAMLIT ===
st.title("☕ FOR REST COFFEE")
st.write("Kelola menu, lihat galeri produk, dan lakukan simulasi transaksi kasir.")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Daftar & Hapus Menu", "➕ Tambah Menu", "💰 Simulasi Kasir", "🖼️ Galeri Foto Menu"])

# --- Ambil Data Menu ---
conn = koneksi_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM menu ORDER BY id ASC")
semua_menu = cursor.fetchall()
conn.close()

# ==========================================
# TAB 1: DAFTAR MENU & FITUR HAPUS
# ==========================================
with tab1:
    st.header("📋 Daftar Menu Saat Ini")
    if semua_menu:
        for baris in semua_menu:
            id_menu = baris[0]
            nama_menu = baris[1]
            harga_menu = baris[2]
            
            kolom_info, kolom_tombol = st.columns([4, 1])
            with kolom_info:
                st.info(f"**ID: {id_menu}** | ☕ **{nama_menu}** | 💵 Rp {harga_menu:,}".replace(",", "."))
            with kolom_tombol:
                if st.button("Hapus", key=f"hapus_{id_menu}"):
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
# TAB 3: SIMULASI KASIR
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
# TAB 4: VISUALISASI GALERI FOTO MENU
# ==========================================
with tab4:
    st.header("🖼️ Galeri Visual Menu Kopi")
    
    kolom1, kolom2 = st.columns(2)
    with kolom1:
        st.image("https://images.unsplash.com/photo-1541167760496-1628856ab772?w=500", 
                 caption="☕ Espresso & Kopi Susu Klasik", use_container_width=True)
        st.caption("*Perpaduan espresso mantap dengan susu lembut, cocok ditemani waktu santai.*")
    with kolom2:
        st.image("https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500", 
                 caption="🧊 Iced Latte Premium", use_container_width=True)
        st.caption("*Kesegaran es kopi latte premium untuk mendinginkan hari yang sibuk.*")

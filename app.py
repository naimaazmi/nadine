import streamlit as st
import os
import glob
from html import escape

# ----------------- KONFIGURASI HALAMAN -----------------
st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia Naima H",
    page_icon="🌸",
    layout="wide"
)

# Folder tempat berkas materi disimpan
DATABASE_DIR = "database"

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

# ----------------- PEMBACAAN OTOMATIS & RELEVANSI MATERI -----------------
BANK_PERTANYAAN_TOPIK = {
    "sastra": "Bagaimana pendekatan struktural dan resepsi sastra dalam membedah karya sastra modern?",
    "apresiasi": "Apa langkah-langkah konkret dalam mengapresiasi dan menganalisis teks puisi serta prosa?",
    "dasar": "Jelaskan hakikat, fungsi, dan ragam kedudukan Bahasa Indonesia sebagai bahasa nasional!",
    "ejaan": "Bagaimana kaidah penggunaan tanda baca koma, titik dua, dan penulisan huruf kapital sesuai pedoman baku?",
    "keterampilan": "Bagaimana korelasi antara keterampilan menyimak kritis dengan kemampuan berbicara dialektis?",
    "morfologi": "Jelaskan perbedaan proses morfologis pembentukan afiksasi prefiks, infiks, sufiks, dan konfiks!",
    "semantik": "Bagaimana cara menganalisis pergeseran makna peyorasi, ameliorasi, dan konotatif dalam wacana?",
    "sintaksis": "Jelaskan fungsi sintaksis subjek, predikat, objek, dan pelengkap dalam kalimat majemuk bertingkat!",
    "wacana": "Bagaimana peranan kohesi gramatikal dan koherensi leksikal dalam menyusun paragraf wacana yang utuh?"
}

def muat_daftar_materi():
    """Membaca folder database secara dinamis."""
    berkas = sorted(glob.glob(os.path.join(DATABASE_DIR, "*.txt")))
    list_materi = []
    
    pilihan_ikon = ["📖", "✍️", "🎙️", "🧩", "📜", "🌐", "📐", "🎭", "💡", "📝", "📚", "🔍"]
    
    for idx, path in enumerate(berkas):
        nama_file = os.path.basename(path)
        nama_bersih = os.path.splitext(nama_file)[0].replace("_", " ").title()
        ikon = pilihan_ikon[idx % len(pilihan_ikon)]
        
        kata_kunci = os.path.splitext(nama_file)[0].lower()
        pertanyaan_cocok = None
        for kunci, tanya in BANK_PERTANYAAN_TOPIK.items():
            if kunci in kata_kunci:
                pertanyaan_cocok = tanya
                break
        if not pertanyaan_cocok:
            pertanyaan_cocok = f"Jelaskan prinsip dasar, teori, dan contoh implementasi mengenai {nama_bersih}!"
        
        list_materi.append({
            "path": path,
            "nama": nama_bersih,
            "ikon": ikon,
            "contoh_tanya": pertanyaan_cocok
        })
    return list_materi

def ambil_konten(filepath):
    """Membaca isi berkas materi."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                konten = f.read().strip()
                return konten if konten else "Materi pada berkas ini masih kosong."
        except Exception as e:
            return f"Terjadi kendala saat membaca materi: {e}"
    return "Berkas materi tidak ditemukan."

def cari_jawaban_di_database(pertanyaan, daftar_materi):
    """Mencari isi materi yang paling relevan berdasarkan pertanyaan pengguna."""
    if not daftar_materi:
        return "Belum ada berkas materi di folder database."

    pertanyaan_lower = pertanyaan.lower()
    kata_kunci_list = [k for k in pertanyaan_lower.split() if len(k) > 2]

    materi_terkait = []

    for materi in daftar_materi:
        nama_materi = materi["nama"].lower()
        konten = ambil_konten(materi["path"])
        konten_lower = konten.lower()

        skor = 0
        for kata in kata_kunci_list:
            if kata in nama_materi:
                skor += 3
            if kata in konten_lower:
                skor += 1

        if skor > 0:
            materi_terkait.append((skor, materi["nama"], konten))

    materi_terkait.sort(key=lambda x: x[0], reverse=True)

    if materi_terkait:
        hasil_text = []
        for _, nama, isi in materi_terkait[:2]:
            hasil_text.append(f"📌 **Materi Terkait: {nama}**\n\n{isi}")
        return "\n\n---\n\n".join(hasil_text)
    else:
        # Jika tidak ditemukan kata kunci spesifik, tampilkan materi pertama sebagai rujukan
        m1 = daftar_materi[0]
        isi1 = ambil_konten(m1["path"])
        return f"Jawaban spesifik tidak ditemukan. Berikut referensi dari materi **{m1['nama']}**:\n\n{isi1}"

# Muat data materi aktif
materi_aktif = muat_daftar_materi()
total_materi = len(materi_aktif)

# Inisialisasi state interaksi
if "teks_pertanyaan" not in st.session_state:
    st.session_state.teks_pertanyaan = ""
if "jawaban_tutor" not in st.session_state:
    st.session_state.jawaban_tutor = None
if "tampilkan_daftar_materi" not in st.session_state:
    st.session_state.tampilkan_daftar_materi = False

# ----------------- CSS STYLING -----------------
st.markdown("""
<style>
    html, body, .stApp, .stApp p, .stApp div, .stApp span, .stApp label,
    .stApp button, .stApp textarea, .stApp input, .stApp h1, .stApp h2,
    .stApp h3, .stApp h4, .stApp li {
        font-family: 'Times New Roman', Times, serif !important;
    }

    .stApp {
        background-color: #fdf2f6;
        color: #3b1f2b;
    }

    .main-wrapper {
        max-width: 900px;
        margin: 0 auto;
        padding-bottom: 50px;
    }

    .greeting-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #f8bbd0;
        padding: 6px 20px;
        border-radius: 25px;
        font-size: 0.95rem;
        color: #ad1457;
        font-style: italic;
        margin-bottom: 15px;
    }

    .hero-banner {
        background: rgba(255, 255, 255, 0.92);
        border: 2px solid #f48fb1;
        border-radius: 24px;
        padding: 24px 30px;
        margin-bottom: 25px;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: bold;
        color: #880e4f;
        margin: 0 0 8px 0;
    }

    .card-info {
        background: rgba(255, 255, 255, 0.92);
        border: 1.5px solid #f48fb1;
        border-left: 6px solid #ad1457;
        border-radius: 16px;
        padding: 16px 22px;
        margin-bottom: 14px;
    }

    .card-info-title {
        font-size: 1.15rem;
        font-weight: bold;
        color: #880e4f;
        margin-bottom: 4px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #a63a58 0%, #7d1c37 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 30px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# Header Utama
st.markdown('<div class="greeting-pill">🌸 Selamat Datang • AI Tutor Bahasa Indonesia Naima H ✨</div>', unsafe_allow_html=True)
st.markdown(f'''
<div class="hero-banner">
    <h1 class="main-title">AI Tutor Bahasa Indonesia Naima H</h1>
    <p>Terhubung otomatis dengan {total_materi} materi pembelajaran di dalam basis data Anda.</p>
</div>
''', unsafe_allow_html=True)

# Form Tanya Jawab
st.markdown('''
<div class="card-info">
    <div class="card-info-title">💬 Ajukan Pertanyaan kepada AI Tutor</div>
    <div>Tuliskan konsep atau kata kunci materi yang ingin Anda pelajari di bawah ini:</div>
</div>
''', unsafe_allow_html=True)

pertanyaan_user = st.text_area(
    label="Kotak Pertanyaan",
    value=st.session_state.teks_pertanyaan,
    placeholder="Ketik pertanyaan atau kata kunci materi (misal: ejaan, sastra, morfologi)...",
    height=100,
    label_visibility="collapsed"
)

col_a1, col_a2 = st.columns([3, 1])
with col_a1:
    if st.button("➤ AJUKAN SEKARANG"):
        if pertanyaan_user.strip():
            with st.spinner("🌸 AI Tutor Naima H sedang menelaah basis data materi Anda..."):
                jawaban = cari_jawaban_di_database(pertanyaan_user, materi_aktif)
                st.session_state.jawaban_tutor = jawaban
        else:
            st.warning("Silakan tuliskan pertanyaan atau kata kunci terlebih dahulu! 💕")

with col_a2:
    if st.button("🔄 Bersihkan"):
        st.session_state.teks_pertanyaan = ""
        st.session_state.jawaban_tutor = None
        st.rerun()

# Menampilkan Hasil Jawaban
if st.session_state.jawaban_tutor:
    st.markdown('''
    <div class="card-info" style="background:#fffafc; border-left-color:#2e7d32; margin-top:20px;">
        <div class="card-info-title" style="color:#2e7d32;">📖 Uraian Hasil Penelusuran Basis Data</div>
    </div>
    ''', unsafe_allow_html=True)
    st.info(st.session_state.jawaban_tutor)

st.markdown('</div>', unsafe_allow_html=True)

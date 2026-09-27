def cari_jawaban_di_database(pertanyaan, daftar_materi):
    """Mencari isi materi yang paling relevan berdasarkan pertanyaan pengguna."""
    if not daftar_materi:
        return "Belum ada berkas materi di folder database."

    pertanyaan_lower = pertanyaan.lower()
    
    # Abaikan kata-kata umum agar fokus pada kata kunci utama (wacana, analisis, dll.)
    stop_words = {"adalah", "yang", "dan", "atau", "dari", "pada", "untuk", "dengan", "apa", "itu", "bagaimana", "mengapa"}
    kata_kunci_list = [k for k in pertanyaan_lower.split() if len(k) > 2 and k not in stop_words]

    if not kata_kunci_list:
        kata_kunci_list = [k for k in pertanyaan_lower.split() if len(k) > 2]

    materi_terkait = []

    for materi in daftar_materi:
        nama_materi = materi["nama"].lower()
        konten = ambil_konten(materi["path"])
        konten_lower = konten.lower()

        skor = 0
        for kata in kata_kunci_list:
            if kata in nama_materi:
                skor += 5  # Bobot kata kunci pada judul materi
            if kata in konten_lower:
                skor += 1

        if skor > 0:
            materi_terkait.append((skor, materi["nama"], konten))

    # Urutkan berdasarkan skor tertinggi
    materi_terkait.sort(key=lambda x: x[0], reverse=True)

    if materi_terkait:
        # Hanya ambil 1 materi terbaik yang paling sesuai dengan pertanyaan
        materi_terbaik = materi_terkait[0]
        return f"📌 **Materi Terkait: {materi_terbaik[1]}**\n\n{materi_terbaik[2]}"
    else:
        m1 = daftar_materi[0]
        isi1 = ambil_konten(m1["path"])
        return f"Sistem tidak menemukan kata kunci yang spesifik. Berikut referensi dari materi **{m1['nama']}**:\n\n{isi1}"

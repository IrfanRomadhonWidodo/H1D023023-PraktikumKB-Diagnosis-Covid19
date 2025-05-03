# Sistem Pakar Deteksi COVID-19

> Developed by **Irfan Romadhon Widodo** (H1D023023)

## 📋 Deskripsi Proyek

Sistem Pakar Deteksi COVID-19 adalah aplikasi berbasis Python dengan antarmuka grafis (GUI) yang dirancang untuk membantu pengguna melakukan skrining awal gejala COVID-19. Sistem ini menggunakan pendekatan berbasis aturan (rule-based system) dan penerapan bobot pada gejala untuk menentukan tingkat kecurigaan seseorang terpapar virus COVID-19.

Aplikasi ini menggabungkan teknologi:
- **Python** dengan **Tkinter** untuk antarmuka pengguna
- **Prolog** sebagai mesin inferensi untuk basis pengetahuan (dengan fallback ke implementasi Python)
- Sistem berbasis bobot untuk analisis gejala

## 🌟 Fitur Utama

- **Antarmuka Pengguna Intuitif** - Desain yang ramah pengguna dengan animasi dan visualisasi interaktif
- **Evaluasi Berbasis Bobot** - Setiap gejala dan faktor risiko memiliki bobot berbeda untuk analisis yang lebih akurat
- **Diagnosis Bertingkat** - Hasil diagnosis dikategorikan dalam beberapa tingkat kecurigaan (Tinggi, Sedang, Rendah)
- **Rekomendasi Spesifik** - Saran tindak lanjut berdasarkan tingkat kecurigaan hasil diagnosis
- **Dual-engine Processing** - Menggunakan Prolog sebagai mesin inferensi utama dengan fallback ke implementasi Python

## 🔧 Teknologi yang Digunakan

- **Frontend**: Python Tkinter
- **Processing Engine**: SWI-Prolog dan Python
- **Knowledge Base**: File Prolog (.pl) untuk aturan dan basis pengetahuan

## 📁 Struktur File

- **covid_expert_system.py** - Aplikasi utama dengan antarmuka GUI dan logika sistem
- **covid_rules.pl** - Basis pengetahuan dan aturan dalam format Prolog

## ⚙️ Cara Penggunaan

1. **Pastikan Prasyarat Terpenuhi**:
   - Python 3.x
   - SWI-Prolog (opsional, aplikasi akan tetap berjalan tanpa Prolog)
   - Library Python: tkinter (biasanya sudah terintegrasi dengan Python)

2. **Jalankan Aplikasi**:
   ```bash
   python covid_expert_system.py
   ```

3. **Ikuti Langkah di Aplikasi**:
   - Isi data diri pada form yang tersedia
   - Jawab pertanyaan terkait gejala dan faktor risiko
   - Lihat hasil diagnosis dan rekomendasi tindak lanjut

## 🧠 Metode Sistem Pakar

Sistem ini mengimplementasikan metode forward chaining dengan kalkulasi bobot pada setiap gejala dan faktor risiko:

- **Gejala Kritis** (bobot 3-4): Demam, batuk kering, sesak napas, kehilangan penciuman/perasa
- **Gejala Umum** (bobot 1-2): Kelelahan, sakit tenggorokan, sakit kepala, nyeri otot, dll.
- **Faktor Risiko** (bobot 4-5): Riwayat kontak dengan pasien COVID-19, perjalanan ke zona merah

Sistem juga melakukan deteksi gejala khas COVID-19 (sesak napas dan kehilangan penciuman/perasa) untuk meningkatkan akurasi diagnosis.

## 📝 Penjelasan Basis Pengetahuan

File `covid_rules.pl` berisi aturan-aturan Prolog yang merupakan basis pengetahuan sistem, meliputi:
- Definisi gejala dan bobotnya
- Definisi faktor risiko dan bobotnya
- Aturan diagnosis berdasarkan total bobot dan kombinasi gejala
- Predikat-predikat pembantu untuk inferensi

## 🔄 Fallback Mechanism

Sistem dirancang dengan mekanisme fallback:
1. Sistem mencoba menggunakan SWI-Prolog untuk inferensi diagnosis
2. Jika SWI-Prolog tidak tersedia, sistem akan otomatis beralih ke implementasi Python
3. Tidak ada perbedaan hasil yang signifikan antara kedua metode

## ⚠️ Disclaimer

Sistem pakar ini dirancang untuk tujuan edukatif dan skrining awal semata. Hasil diagnosis **tidak menggantikan** pemeriksaan medis oleh tenaga kesehatan profesional. Selalu konsultasikan dengan dokter untuk diagnosis yang akurat.

## 📊 Tentang Pembobotan

Pembobotan dalam sistem ini didasarkan pada frekuensi dan spesifisitas gejala COVID-19 berdasarkan literatur medis. Semakin spesifik suatu gejala terhadap COVID-19, semakin tinggi bobotnya.

## 🧑‍💻 Tentang Pengembang

Proyek ini dikembangkan oleh Irfan Romadhon Widodo (H1D023023) sebagai implementasi sistem pakar berbasis aturan dengan antarmuka grafis modern.

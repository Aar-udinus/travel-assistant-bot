🌍 Travel Assistant Bot

Chatbot Perjalanan Berbasis Gemini 2.5 Flash dengan UI Elegan + Multimodal (Gambar)

Travel Assistant Bot adalah aplikasi chatbot cerdas berbasis Google Gemini API yang dirancang untuk membantu pengguna merencanakan perjalanan secara cepat, akurat, dan modern.
Dilengkapi dengan antarmuka super elegan, preset pertanyaan, penyimpan rencana perjalanan, dan dukungan upload gambar (multimodal).

✨ Fitur Utama
1. Chatbot Travel Assistant

Memberikan rekomendasi perjalanan, itinerary, tips transportasi, estimasi budget, dan saran keselamatan.

2. UI Premium & Elegan
- Background gradasi
- Chat bubble modern
- Kartu preset informatif
- Panel rencana perjalanan

3. Pengaturan Jawaban

- Pilihan gaya bahasa: Santai, Detail, Semi Formal
- Pengaturan kedalaman penjelasan (1–5)

4. Preset Pertanyaan Cepat
Tinggal klik — langsung dikirim ke bot:
- Bali 3 Hari
- Jogja Hemat
- Honeymoon
- Solo Traveler

5. Dukungan Upload Gambar (Multimodal)
- Unggah gambar seperti:
- Tiket pesawat/kereta
- Foto tempat wisata
- Screenshot peta
- Foto makanan/menu
Bot akan menganalisis gambar dan menjawab berdasarkan isinya.

6. Simpan Rencana Perjalanan
- Hasil chat bisa disimpan dan dibaca kembali.

Instalasi & Menjalankan

1️⃣ Clone repo git clone https://github.com/username/travel-assistant-bot.git
    cd travel-assistant-bot
    
2️⃣ Install dependencies
    - Pastikan Python 3.9+ sudah terpasang.
    - pip install -r requirements.txt
    
3️⃣ Jalankan aplikasi
    streamlit run app.py
    
4️⃣ Masukkan Gemini API Key
   API key bisa diperoleh dari:
  - 🔗https://aistudio.google.com
  -  Masukkan API KEY ke sidebar aplikasi.
    
📁 Struktur Proyek travel-assistant-bot/
│
├── app.py                # File utama Streamlit
├── requirements.txt      # Dependency Python
├── README.md             # Dokumentasi ini
└── screenshots/          # Folder screenshot UI (opsional)

🔑 Teknologi yang Digunakan
- Teknologi	Keterangan
- Streamlit	Framework UI Python untuk web apps
- Gemini 2.5 Flash	Model AI Google terbaru (multimodal)
- google-genai	SDK resmi Gemini

🧠 Cara Kerja Multimodal
  - Pengguna dapat meng-upload gambar (jpg/jpeg/png).
    Aplikasi akan:
    1.Menyimpan sementara ke file temp
    2.Upload gambar ke Gemini API
    3.Mengirim prompt + gambar ke model
    4.Mendapat jawaban berdasarkan analisis visual + konteks teks



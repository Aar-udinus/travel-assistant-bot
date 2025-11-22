import streamlit as st
import tempfile
from google import genai
from google.genai import types
from google.api_core.exceptions import GoogleAPIError

# =========================
# 🔧 CONFIG DASAR APLIKASI
# =========================
st.set_page_config(
    page_title="🌍 Travel Assistant Bot",
    page_icon="🌍",
    layout="wide"
)

# =========================
# 🎨 CUSTOM CSS (UI ELEGAN)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #e0f7fa 0, #ffffff 40%, #f3e5f5 100%);
        font-family: "Segoe UI", Roboto, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1976d2 40%, #42a5f5 100%);
        color: white;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p {
        color: #e3f2fd !important;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #455a64;
        margin-bottom: 1rem;
    }
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 1.2rem;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 12px 30px rgba(15, 76, 129, 0.12);
        border: 1px solid #e3f2fd;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        background: #e3f2fd;
        color: #0d47a1;
    }
    .badge-dot {
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: #4caf50;
        box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.25);
    }
    .chat-bubble {
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        margin-bottom: 0.4rem;
        max-width: 100%;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    .chat-user {
        background: #e3f2fd;
        margin-left: auto;
        border-bottom-right-radius: 0.3rem;
    }
    .chat-assistant {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        margin-right: auto;
        border-bottom-left-radius: 0.3rem;
    }
    .chat-container {
        padding: 0.75rem 0.5rem;
    }
    .hint {
        font-size: 0.78rem;
        color: #78909c;
        margin-top: 0.4rem;
    }
    .preset-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #37474f;
        margin-bottom: 0.2rem;
    }
    .preset-desc {
        font-size: 0.78rem;
        color: #78909c;
        margin-bottom: 0.6rem;
    }
    .preset-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 1rem;
        padding: 0.8rem;
        box-shadow: 0 6px 16px rgba(15, 76, 129, 0.10);
        border: 1px solid #e3f2fd;
        height: 100%;
    }
    .preset-card-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .preset-card-text {
        font-size: 0.8rem;
        color: #607d8b;
        margin-bottom: 0.6rem;
    }
    .plan-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 0.9rem;
        padding: 0.7rem 0.9rem;
        box-shadow: 0 4px 12px rgba(15, 76, 129, 0.10);
        border: 1px solid #e3f2fd;
        margin-bottom: 0.6rem;
        font-size: 0.82rem;
        max-height: 220px;
        overflow-y: auto;
    }
    .plan-title {
        font-size: 0.86rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
        color: #1a237e;
    }
    .plan-meta {
        font-size: 0.72rem;
        color: #78909c;
        margin-bottom: 0.3rem;
    }
    .small-muted {
        font-size: 0.75rem;
        color: #90a4ae;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 🤖 SYSTEM INSTRUCTION
# =========================
SYSTEM_INSTRUCTION = """
Anda adalah Travel Assistant Bot, seorang Asisten Perjalanan Digital.
Gaya bicara: Santai, ramah, sopan, dan informatif.
Fokus Anda adalah memberikan rekomendasi destinasi wisata, itinerary perjalanan,
tips transportasi, estimasi budget, serta saran persiapan dan keamanan.
Jika tidak yakin, akui dengan sopan dan beri alternatif rekomendasi yang masuk akal.
Selalu gunakan bahasa Indonesia.
"""

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION
)

# =========================
# 🧠 STATE AWAL
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = None
if "client" not in st.session_state:
    st.session_state.client = None
if "saved_plans" not in st.session_state:
    st.session_state.saved_plans = []
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

# =========================
# 🎛 SIDEBAR: API & SETTINGS
# =========================
st.sidebar.title("🔑 Pengaturan")
st.sidebar.markdown("Masukkan **Gemini API Key** untuk mulai menggunakan bot.")

api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    help="API key bisa didapat dari Google AI Studio."
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Preferensi Jawaban")
tone = st.sidebar.selectbox(
    "Gaya Jawaban",
    ["Santai & Singkat", "Santai & Detail", "Semi Formal"],
    index=1
)

detail_level = st.sidebar.slider(
    "Tingkat Kedalaman Jawaban",
    1, 5, 3,
    help="1 = sangat ringkas, 5 = sangat detail."
)

st.sidebar.markdown("---")
st.sidebar.caption("💡 Tips: Jaga API key kamu, jangan di-share ke publik 😉")

# =========================
# ☁️ HEADER UTAMA
# =========================
top_left, top_right = st.columns([2.5, 1.5])

with top_left:
    st.markdown(
        """
        <div class="main-title">🌍 Travel Assistant Bot</div>
        <div class="main-subtitle">
            Teman ngobrol buat merencanakan liburanmu — dari itinerary, budget, sampai tips lokal.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="badge">
                <div class="badge-dot"></div>
                Travel Mode: Aktif
            </div>
            <br/><br/>
            <b>Contoh yang bisa kamu tanyakan:</b>
            <ul>
                <li>“Buatkan itinerary 4 hari 3 malam ke Jogja dengan budget hemat.”</li>
                <li>“Bandingkan liburan ke Bali vs Labuan Bajo untuk honeymoon.”</li>
                <li>“Tips naik kereta malam dari Jakarta ke Surabaya.”</li>
            </ul>
            <span class="small-muted">
                Semakin detail kamu menjelaskan (jumlah orang, tanggal, preferensi), semakin akurat rekomendasinya ✨
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with top_right:
    st.markdown(
        """
        <div class="info-card">
            <b>Status Koneksi</b><br/>
        """,
        unsafe_allow_html=True
    )
    if api_key:
        st.markdown(
            """
            <span class="badge">
                <div class="badge-dot"></div>
                API Key terisi
            </span>
            <p style="font-size:0.8rem; margin-top:0.6rem;">
                Siap membantu kamu merencanakan perjalanan ✈️
            </p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <span class="badge" style="background:#ffebee; color:#b71c1c;">
                ! API Key kosong
            </span>
            <p style="font-size:0.8rem; margin-top:0.6rem;">
                Masukkan API key di sidebar untuk mengaktifkan bot.
            </p>
            """,
            unsafe_allow_html=True
        )
    if st.session_state.saved_plans:
        st.markdown(
            f"""
            <p style="font-size:0.8rem; margin-top:0.4rem;">
                📂 Rencana tersimpan: <b>{len(st.session_state.saved_plans)}</b>
            </p>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# 🚀 INISIALISASI CLIENT & CHAT
# =========================
def init_client_and_chat(key: str):
    try:
        client = genai.Client(api_key=key)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=config,
        )
        return client, chat, None
    except Exception as e:
        return None, None, str(e)

if api_key and st.session_state.chat is None:
    client, chat, err = init_client_and_chat(api_key)
    if err:
        st.error(f"Error inisialisasi: {err}")
    else:
        st.session_state.client = client
        st.session_state.chat = chat
        st.rerun()

# =========================
# 🧠 FUNGSI BANTU
# =========================
def build_prompt(user_prompt: str) -> str:
    extra_style = ""
    if tone == "Santai & Singkat":
        extra_style = "Jawab dengan santai, ringkas, dan langsung ke poin."
    elif tone == "Santai & Detail":
        extra_style = "Jawab dengan santai, cukup detail, gunakan poin-poin bila perlu."
    elif tone == "Semi Formal":
        extra_style = "Jawab dengan bahasa semi formal, tetap hangat dan jelas."

    depth_text = f"Tingkat kedalaman penjelasan: {detail_level} dari 5."
    return f"{extra_style}\n{depth_text}\n\nPertanyaan pengguna: {user_prompt}"

def generate_response(prompt: str, uploaded_image=None) -> str:
    try:
        chat = st.session_state.chat

        # Jika ada gambar, upload ke Gemini dan kirim teks + gambar
        if uploaded_image is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_image.getbuffer())
                tmp_path = tmp.name

            gemini_file = st.session_state.client.files.upload(file=tmp_path)
            contents = [prompt, gemini_file]
            response = chat.send_message(contents)
        else:
            response = chat.send_message(prompt)

        return response.text

    except GoogleAPIError as e:
        return f"Terjadi kesalahan API: {e.message}"
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi API: {e}"

# =========================
# 🔘 PRESET PERTANYAAN
# =========================
preset_prompt = None

st.markdown("### ✨ Preset Pertanyaan Cepat")
st.markdown(
    """
    <div class="preset-title">Butuh inspirasi? Klik salah satu preset di bawah ini.</div>
    <div class="preset-desc">Pertanyaan akan otomatis dikirim ke bot seperti kamu mengetik sendiri.</div>
    """,
    unsafe_allow_html=True
)

pcol1, pcol2, pcol3, pcol4 = st.columns(4)

with pcol1:
    st.markdown('<div class="preset-card">', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-title">🏝️ Bali 3 Hari</div>', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-text">Itinerary santai untuk 2 orang dengan budget menengah.</div>', unsafe_allow_html=True)
    if st.button("Gunakan", key="preset_bali", use_container_width=True):
        preset_prompt = "Buatkan itinerary 3 hari 2 malam ke Bali untuk 2 orang dengan budget menengah."
    st.markdown('</div>', unsafe_allow_html=True)

with pcol2:
    st.markdown('<div class="preset-card">', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-title">🏰 Jogja Hemat</div>', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-text">Liburan mahasiswa hemat 3 hari 2 malam.</div>', unsafe_allow_html=True)
    if st.button("Gunakan", key="preset_jogja", use_container_width=True):
        preset_prompt = "Rancang liburan hemat 3 hari 2 malam di Yogyakarta untuk 4 orang mahasiswa."
    st.markdown('</div>', unsafe_allow_html=True)

with pcol3:
    st.markdown('<div class="preset-card">', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-title">💞 Honeymoon</div>', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-text">Destinasi romantis di Indonesia + itinerary.</div>', unsafe_allow_html=True)
    if st.button("Gunakan", key="preset_honeymoon", use_container_width=True):
        preset_prompt = "Rekomendasikan destinasi honeymoon di Indonesia dan buatkan itinerary 5 hari."
    st.markdown('</div>', unsafe_allow_html=True)

with pcol4:
    st.markdown('<div class="preset-card">', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-title">🎒 Solo Traveler</div>', unsafe_allow_html=True)
    st.markdown('<div class="preset-card-text">Kota ramah pemula + tips keamanan.</div>', unsafe_allow_html=True)
    if st.button("Gunakan", key="preset_solo", use_container_width=True):
        preset_prompt = "Berikan rekomendasi kota di Indonesia yang cocok untuk solo traveler pemula beserta tipsnya."
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# LAYOUT BAWAH: CHAT & RENCANA TERSIMPAN
# =========================
chat_col, saved_col = st.columns([2.4, 1.6])

# =========================
# 🗨️ AREA CHAT
# =========================
with chat_col:
    st.markdown("### 💬 Percakapan")

    # 📸 Upload gambar (opsional)
    uploaded_image = st.file_uploader(
        "📸 Upload gambar terkait perjalanan (opsional)",
        type=["jpg", "jpeg", "png"],
        help="Unggah tiket, foto tempat wisata, screenshot maps, menu, dll."
    )

    if uploaded_image:
        st.image(uploaded_image, caption="Gambar terunggah", use_column_width=True)

    chat_container = st.container()
    with chat_container:
        if st.session_state.chat is not None:
            history = st.session_state.chat.get_history()
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in history:
                role = "user" if msg.role == "user" else "assistant"
                bubble_class = "chat-user" if role == "user" else "chat-assistant"
                with st.chat_message(role):
                    st.markdown(
                        f'<div class="chat-bubble {bubble_class}">{msg.parts[0].text}</div>',
                        unsafe_allow_html=True
                    )
            st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.chat is not None:
        placeholder_text = "Contoh: Susun itinerary 3 hari ke Bandung untuk liburan keluarga."
        typed_prompt = st.chat_input(placeholder_text)

        st.markdown(
            """
            <div class="hint">
                💡 Tip: Tambahkan detail seperti jumlah orang, tanggal, preferensi wisata, dan budget agar saran lebih akurat.
            </div>
            """,
            unsafe_allow_html=True
        )

        effective_prompt = None
        if preset_prompt:
            effective_prompt = preset_prompt
        elif typed_prompt:
            effective_prompt = typed_prompt

        if effective_prompt:
            with st.chat_message("user"):
                st.markdown(
                    f'<div class="chat-bubble chat-user">{effective_prompt}</div>',
                    unsafe_allow_html=True
                )

            styled_prompt = build_prompt(effective_prompt)

            with st.chat_message("assistant"):
                with st.spinner("Travel Assistant sedang menyusun rekomendasi..."):
                    answer = generate_response(styled_prompt, uploaded_image=uploaded_image)
                    st.session_state.last_answer = answer
                    st.markdown(
                        f'<div class="chat-bubble chat-assistant">{answer}</div>',
                        unsafe_allow_html=True
                    )
    else:
        with chat_col:
            st.info("Silakan masukkan API Key di sebelah kiri untuk memulai percakapan ✨")

# =========================
# 📂 PANEL RENCANA TERSIMPAN
# =========================
with saved_col:
    st.markdown("### 📂 Rencana Perjalanan Tersimpan")

    if st.session_state.last_answer:
        if st.button("💾 Simpan jawaban terakhir sebagai rencana", use_container_width=True):
            title = f"Rencana #{len(st.session_state.saved_plans) + 1}"
            st.session_state.saved_plans.append({
                "title": title,
                "content": st.session_state.last_answer
            })
            st.success("Rencana berhasil disimpan.")

    if st.session_state.saved_plans:
        for idx, plan in enumerate(st.session_state.saved_plans, start=1):
            st.markdown('<div class="plan-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="plan-title">{plan["title"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="plan-meta">🧳 Disusun oleh Travel Assistant • #{idx}</div>',
                unsafe_allow_html=True
            )
            st.markdown(plan["content"])
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="plan-card">
                <div class="plan-title">Belum ada rencana tersimpan</div>
                <div class="plan-meta">Simpan dulu salah satu jawaban bot untuk melihatnya di sini.</div>
                <p class="small-muted">
                    Gunakan chat di sebelah kiri untuk membuat itinerary, lalu klik tombol <b>"Simpan jawaban terakhir sebagai rencana"</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

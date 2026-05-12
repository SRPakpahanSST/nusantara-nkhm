import streamlit as st
import pandas as pd
import random
from datetime import datetime
import openai
import time

# ========== SPLASH SCREEN ==========
if not st.session_state.get("splash_selesai", False):
    st.set_page_config(page_title="NKHM Nusantara", page_icon="🇮🇩", layout="wide")
    splash_holder = st.empty()
    with splash_holder.container():
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        logo_url = "https://raw.githubusercontent.com/SRPakpahanSST/nusantara-nkhm/main/assets/pmd_logo.jpg"
        st.markdown(f'<img src="{logo_url}" width="180">', unsafe_allow_html=True)
        st.markdown("<h1>NKHM Nusantara</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px;'>Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>Berbasis Perkembangan Data Personal</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <style>
        div.stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 22px;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("🚀 Mulai", use_container_width=True):
            st.session_state.splash_selesai = True
            st.rerun()
    st.stop()

# ========== APLIKASI UTAMA ==========
st.set_page_config(page_title="NKHM Nusantara", page_icon="🇮🇩", layout="wide")

st.markdown("""
<style>
    .stButton > button { width: 100%; font-size: 18px; padding: 10px; }
    .stProgress > div > div { background-color: #4CAF50; }
    h1, h2, h3 { text-align: center; }
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] { font-size: 12px; }
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if "user" not in st.session_state:
    st.session_state.user = ""
if "scores" not in st.session_state:
    st.session_state.scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
if "history" not in st.session_state:
    st.session_state.history = []
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []  # untuk menyimpan percakapan dengan AI

# ========== BANK SOAL (CONTOH, GANTI DENGAN RIBUAN SOAL ANDA) ==========
QUESTION_BANK = [
    {
        "text": "Siapa yang membacakan teks proklamasi kemerdekaan Indonesia?",
        "options": ["Soekarno", "Moh Hatta", "Soekarno-Hatta", "Ahmad Soebarjo"],
        "correct": "Soekarno-Hatta",
        "type": "IQ",
        "national": True
    },
    # ... tambahkan soal Anda di sini ...
]

def calculate_nkhm(iq, eq, sq, aq):
    pembilang = (iq + eq) * (sq + aq)
    penyebut = (iq + eq) + (sq + aq)
    if penyebut == 0:
        return 0
    return round(pembilang / penyebut, 2)

def get_nkhm_level(nkhm):
    if nkhm >= 80:
        return "🌟 Pahlawan Cerdas", "green"
    elif nkhm >= 60:
        return "📚 Cendekia Muda", "blue"
    elif nkhm >= 40:
        return "🌱 Penjelajah Ilmu", "orange"
    else:
        return "🌿 Perintis Jalan", "gray"

# ========== FUNGSI ASISTEN AI SEDERHANA (tanpa langchain) ==========
def get_ai_response(user_input, message_history):
    """Mengirim prompt ke OpenAI dan mengembalikan respons secara streaming."""
    if "OPENAI_API_KEY" not in st.secrets:
        return "Maaf, fitur AI belum diatur. Silakan hubungi administrator."
    
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    
    # Siapkan pesan dengan konteks profil
    scores = st.session_state.scores
    profile_context = (
        f"Pengguna bernama {st.session_state.user}. "
        f"Skor IQ: {scores['IQ']}, EQ: {scores['EQ']}, SQ: {scores['SQ']}, AQ: {scores['AQ']}. "
        f"Total soal dijawab: {st.session_state.total_questions}."
    )
    
    system_prompt = f"""Kamu adalah Ki Hajar, asisten AI yang hangat dan bijaksana di aplikasi NKHM Nusantara. 
Tugasmu membantu pengguna memahami kecerdasan (IQ, EQ, SQ, AQ), memberikan motivasi belajar, merekomendasikan soal, dan menjawab pertanyaan kebangsaan.
Gunakan sapaan ramah. Berikut profil pengguna: {profile_context}
"""
    messages = [{"role": "system", "content": system_prompt}]
    for m in message_history[-10:]:
        messages.append(m)
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            stream=True
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.get("content"):
                content = chunk.choices[0].delta.content
                full_response += content
                yield full_response
                time.sleep(0.02)
    except Exception as e:
        yield f"Maaf, terjadi error: {str(e)}"

# ========== LOGIN ==========
if not st.session_state.user:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://emojis.slackmojis.com/emojis/2020-08-14/5540484763/indonesia_emoji.png?1585564", width=80)
        st.title("🇮🇩 NKHM NUSANTARA")
        st.markdown("### Asah 4 Kecerdasan + Nasionalisme")
        st.markdown("---")
        name = st.text_input("🖊️ Masukkan namamu", placeholder="contoh: Budi Santoso")
        col_a, col_b = st.columns(2)
        with col_a:
            st.caption("🧠 IQ = Intelektual")
            st.caption("❤️ EQ = Emosi")
        with col_b:
            st.caption("🙏 SQ = Spiritual")
            st.caption("💪 AQ = Daya Juang")
        if st.button("🚀 MULAI BELAJAR", use_container_width=True):
            if name and name.strip():
                st.session_state.user = name.strip()
                st.rerun()
            else:
                st.error("Masukkan nama dulu ya!")
else:
    nkhm = calculate_nkhm(
        st.session_state.scores["IQ"],
        st.session_state.scores["EQ"],
        st.session_state.scores["SQ"],
        st.session_state.scores["AQ"]
    )
    nkhm_level, _ = get_nkhm_level(nkhm)
    
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.user}")
        st.markdown("---")
        st.markdown(f"### 🎯 NKHM: **{nkhm}**")
        st.markdown(f"*Level: {nkhm_level}*")
        st.progress(min(nkhm/100, 1.0), text="Progress ke level berikutnya")
        st.markdown("---")
        st.markdown("### 📊 Skor Kecerdasan")
        for t in ["IQ", "EQ", "SQ", "AQ"]:
            st.progress(st.session_state.scores[t]/100, text=f"{t}: {st.session_state.scores[t]}")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📖 Total Soal", st.session_state.total_questions)
        with col2:
            best = max([h.get("nkhm", 0) for h in st.session_state.history] + [nkhm])
            st.metric("🏆 Best NKHM", best)
        if st.button("🔄 Reset Semua Skor", use_container_width=True):
            st.session_state.scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
            st.session_state.history = []
            st.session_state.total_questions = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 🤖 Ki Hajar (AI)")
        # Tampilkan chat history
        for msg in st.session_state.ai_messages:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant", avatar="🤖").write(msg["content"])
        
        user_question = st.chat_input("Tanya Ki Hajar...")
        if user_question:
            st.session_state.ai_messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)
            with st.chat_message("assistant", avatar="🤖"):
                response_placeholder = st.empty()
                full_response = ""
                for chunk in get_ai_response(user_question, st.session_state.ai_messages):
                    full_response = chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            st.session_state.ai_messages.append({"role": "assistant", "content": full_response})
            st.rerun()
    
    # TABS (Kuis, Dashboard, Prestasi) – sama seperti kode Anda sebelumnya
    tab1, tab2, tab3 = st.tabs(["🎮 MAIN KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
    
    with tab1:
        # ... (salin dari kode Anda yang sudah berfungsi) ...
        st.info("Tab Kuis: silakan gunakan kode Anda yang sudah ada")
    
    with tab2:
        st.info("Tab Dashboard: silakan gunakan kode Anda yang sudah ada")
    
    with tab3:
        st.info("Tab Prestasi: silakan gunakan kode Anda yang sudah ada")

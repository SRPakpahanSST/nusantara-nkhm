import streamlit as st
import pandas as pd
import random
from datetime import datetime
import openai
import time

# ========== FUNGSI ASISTEN AI ==========
def get_ai_response(user_input, message_history):
    if "OPENAI_API_KEY" not in st.secrets:
        yield "Maaf, fitur AI belum diatur. Silakan hubungi administrator."
        return
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    scores = st.session_state.scores
    profile_context = (
        f"Pengguna bernama {st.session_state.user}. "
        f"Skor IQ: {scores['IQ']}, EQ: {scores['EQ']}, SQ: {scores['SQ']}, AQ: {scores['AQ']}. "
        f"Total soal: {st.session_state.total_questions}."
    )
    system_prompt = f"""Kamu adalah Ki Hajar, asisten AI di NKHM Nusantara. 
Profil pengguna: {profile_context}
Berikan jawaban ramah, singkat, dan berguna."""
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
        full = ""
        for chunk in response:
            if chunk.choices[0].delta.get("content"):
                content = chunk.choices[0].delta.content
                full += content
                yield full
                time.sleep(0.02)
    except Exception as e:
        yield f"Error: {str(e)}"

# ========== SPLASH SCREEN ==========𝐪𝐩𝐚𝐦𝐲𝐦 𝐥

if not st.session_state.get("splash_selesai", False):
    st.set_page_config(page_title="NKHM Nusantara", page_icon="🇮🇩", layout="wide")

    # Kosongkan area utama
    splash_holder = st.empty()

    with splash_holder.container():
        # ----- Layout 3 kolom untuk center -----
        col_kiri, col_tengah, col_kanan = st.columns([1, 2, 1])
        with col_tengah:
            # 1. Gambar logo (pakai raw URL dari GitHub)
            logo_url = "https://raw.githubusercontent.com/SRPakpahanSST/nusantara-nkhm/main/assets/pmd_logo.jpg"
            st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="180"></div>',
    unsafe_allow_html=True
)
            # 2. Judul "NKHM Nusantara"
            st.markdown(
                "<h1 style='text-align: center;'>NKHM Nusantara</h1>",
                unsafe_allow_html=True,
            )

            # 3. Deskripsi tambahan (baris kedua)
            st.markdown(
                "<p style='text-align: center; font-size: 18px;'>Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>Berbasis Perkembangan Data Personal</p>",
                unsafe_allow_html=True,
            )

            # 4. CSS untuk tombol hijau & besar
            st.markdown(
                """
                <style>
                div.stButton > button {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 22px;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 12px 24px;
                    width: 100%;
                }
                div.stButton > button:hover {
                    background-color: #45a049;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # 5. Tombol "Mulai"
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_selesai = True
                st.rerun()

    # Hentikan eksekusi aplikasi utama sampai tombol ditekan
    st.stop()
    
    # Tempat untuk splash
    splash_holder = st.empty()
    with splash_holder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Tampilkan logo PMD Pakpahan Ministry (jika file ada)
            logo_path = "assets/pmd_logo.jpg"  # Ganti dengan nama file gambar Anda
            if os.path.exists(logo_path):
                st.image(logo_path, width=200)
            else:
                # Fallback teks jika gambar belum diupload
                st.markdown("<h1 style='text-align: center;'>PMD</h1>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center;'>Pakpahan Ministry</h3>", unsafe_allow_html=True)
            
            st.markdown("<h1 style='text-align: center;'>🇮🇩 NKHM Nusantara</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Asah 4 Kecerdasan + Nasionalisme</h3>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center;'>
                <p>🧠 <b>IQ</b> – Kecerdasan Intelektual<br>
                ❤️ <b>EQ</b> – Kecerdasan Emosi<br>
                🙏 <b>SQ</b> – Kecerdasan Spiritual<br>
                💪 <b>AQ</b> – Kecerdasan Daya Juang</p>
                <p>Berbasis nilai kebangsaan dan sejarah Indonesia.</p>
                <p><b>Rumus NKHM:</b> ((IQ+EQ)×(SQ+AQ)) / ((IQ+EQ)+(SQ+AQ))</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
            if st.button("🚀 Mulai Sekarang", use_container_width=True):
                st.session_state.splash_selesai = True
                st.rerun()
    st.stop()

# ========== APLIKASI UTAMA (setelah splash) ==========
st.set_page_config(page_title="NKHM Nusantara", page_icon="🇮🇩", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        font-size: 18px;
        padding: 10px;
    }
    .stProgress > div > div {
        background-color: #4CAF50;
    }
    h1, h2, h3 {
        text-align: center;
    }
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 12px;
        }
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

# ========== BANK SOAL (Contoh, ganti dengan ribuan soal Anda) ==========
QUESTION_BANK = [
    {
        "text": "Siapa yang membacakan teks proklamasi kemerdekaan Indonesia?",
        "options": ["Soekarno", "Moh Hatta", "Soekarno-Hatta", "Ahmad Soebarjo"],
        "correct": "Soekarno-Hatta",
        "type": "IQ",
        "national": True
    },
    # ... Tambahkan semua soal Anda di sini ...
]

# Fungsi NKHM
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
    
    tab1, tab2, tab3 = st.tabs(["🎮 MAIN KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
    
    # Tab Kuis (sama seperti sebelumnya, potongan di bawah)
    with tab1:
        st.markdown("### 🎮 Pilih Kuis")
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            kategori = st.radio("🏷️ Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], horizontal=True)
        with filter_col2:
            kecerdasan = st.selectbox("🧠 Fokus Kecerdasan", ["Semua", "IQ", "EQ", "SQ", "AQ"])
        
        filtered = QUESTION_BANK.copy()
        if kategori == "🇮🇩 Nasionalisme":
            filtered = [q for q in filtered if q["national"]]
        elif kategori == "📚 Umum":
            filtered = [q for q in filtered if not q["national"]]
        if kecerdasan != "Semua":
            filtered = [q for q in filtered if q["type"] == kecerdasan]
        
        if not filtered:
            st.warning("Tidak ada soal dengan filter ini. Coba filter lain!")
        else:
            if "current_q" not in st.session_state:
                st.session_state.current_q = random.choice(filtered)
                st.session_state.answered = False
            
            q = st.session_state.current_q            
            with st.container():
                st.markdown("---")
                st.markdown(f"### 📝 {q['text']}")
                col_tag1, col_tag2, col_tag3 = st.columns(3)
                with col_tag1:
                    st.info(f"🧠 {q['type']}")
                with col_tag2:
                    if q['national']:
                        st.success("🇮🇩 Nasional")
                    else:
                        st.info("📚 Umum")
                with col_tag3:
                    st.caption("+10 poin" if not st.session_state.answered else "✅ Sudah dijawab")
                st.markdown("---")
                selected = st.radio("Pilih jawabanmu:", q['options'], key=f"q_{q['text']}_{st.session_state.answered}", disabled=st.session_state.answered)
                if st.button("✅ JAWAB", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    st.session_state.total_questions += 1
                    if selected == q['correct']:
                        st.session_state.scores[q['type']] = min(100, st.session_state.scores[q['type']] + 10)
                        st.success(f"✅ **BENAR!** +10 poin untuk {q['type']}")
                    else:
                        st.error(f"❌ **SALAH!** Jawaban benar: **{q['correct']}**")
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50] + "...",
                        "type": q['type'],
                        "correct": selected == q['correct'],
                        "nkhm": calculate_nkhm(
                            st.session_state.scores["IQ"],
                            st.session_state.scores["EQ"],
                            st.session_state.scores["SQ"],
                            st.session_state.scores["AQ"]
                        )
                    })
                    if st.button("⏩ SOAL SELANJUTNYA", use_container_width=True):
                        st.session_state.current_q = random.choice(filtered)
                        st.session_state.answered = False
                        st.rerun()
                if st.session_state.answered:
                    if st.button("🎮 Kuis Baru", use_container_width=True):
                        st.session_state.current_q = random.choice(filtered)
                        st.session_state.answered = False
                        st.rerun()
    
    with tab2:
        st.markdown("### 📊 Dashboard Perkembangan")
        df_chart = pd.DataFrame({
            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ"],
            "Skor": [st.session_state.scores["IQ"], st.session_state.scores["EQ"], st.session_state.scores["SQ"], st.session_state.scores["AQ"]]
        })
        st.bar_chart(df_chart.set_index("Kecerdasan"), height=300)
        st.markdown("### 📝 Rekomendasi Peningkatan")
        lowest = min(st.session_state.scores, key=st.session_state.scores.get)
        if st.session_state.scores[lowest] < 50:
            st.info(f"💡 **Tingkatkan {lowest}:** Latihan lebih giat di bagian {lowest}!")
        else:
            st.success("🌟 Semua kecerdasan sudah terasah dengan baik!")
        if st.session_state.history:
            st.markdown("### 📜 Riwayat Kuis (10 Terakhir)")
            history_df = pd.DataFrame(st.session_state.history[-10:])
            history_df = history_df[["timestamp", "type", "question", "correct"]]
            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
            history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil"]
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 🏆 Pencapaianmu")
        cols = st.columns(4)
        badges = {"IQ": "🧠 Cendekia", "EQ": "❤️ Empati", "SQ": "🙏 Bhinneka", "AQ": "💪 Tangguh"}
        for i, (t, label) in enumerate(badges.items()):
            if st.session_state.scores[t] >= 50:
                cols[i].success(f"✅ **{label}**")
            else:
                cols[i].info(f"🔒 {label} (butuh 50)")
        if all(st.session_state.scores[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ"]):
            st.balloons()
            st.success("🎉 **GELAR: PAHLAWAN CERDAS NUSANTARA!** 🎉")
        st.markdown("---")
        answered = len(st.session_state.history)
        correct = sum(1 for h in st.session_state.history if h["correct"])
        accuracy = (correct / answered * 100) if answered > 0 else 0
        col1, col2, col3 = st.columns(3)
        col1.metric("📖 Total Soal", answered)
        col2.metric("✅ Benar", correct)
        col3.metric("📊 Akurasi", f"{accuracy:.1f}%")

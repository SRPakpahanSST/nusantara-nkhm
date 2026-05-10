import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="NKHM Nusantara",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

if "user" not in st.session_state:
    st.session_state.user = ""
if "scores" not in st.session_state:
    st.session_state.scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
if "history" not in st.session_state:
    st.session_state.history = []
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

#from questions import QUESTION_BANK
QUESTION_BANK = [
    {
        "text": "Siapa yang membacakan teks proklamasi?",
        "options": ["Soekarno", "Moh Hatta", "Soekarno-Hatta", "Ahmad Soebarjo"],
        "correct": "Soekarno-Hatta",
        "type": "IQ",
        "national": True
    },
    # ... soal lainnya
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
    nkhm_level, level_color = get_nkhm_level(nkhm)
    
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.user}")
        st.markdown("---")
        st.markdown(f"### 🎯 NKHM: **{nkhm}**")
        st.markdown(f"*Level: {nkhm_level}*")
        st.progress(min(nkhm/100, 1.0), text=f"Progress ke level berikutnya")
        st.markdown("---")
        st.markdown("### 📊 Skor Kecerdasan")
        for t in ["IQ", "EQ", "SQ", "AQ"]:
            st.progress(st.session_state.scores[t]/100, text=f"{t}: {st.session_state.scores[t]}")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📖 Total Soal", st.session_state.total_questions)
        with col2:
            st.metric("🏆 Best NKHM", max([h.get("nkhm", 0) for h in st.session_state.history] + [nkhm]))
        if st.button("🔄 Reset Semua Skor", use_container_width=True):
            st.session_state.scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
            st.session_state.history = []
            st.session_state.total_questions = 0
            st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["🎮 MAIN KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
    
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
                    point_display = "+10 poin" if not st.session_state.answered else "✅ Sudah dijawab"
                    st.caption(point_display)
                st.markdown("---")
                
                selected = st.radio(
                    "Pilih jawabanmu:",
                    q['options'],
                    key=f"q_{q['text']}_{st.session_state.answered}",
                    disabled=st.session_state.answered
                )
                
                if st.button("✅ JAWAB", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    st.session_state.total_questions += 1
                    
                    if selected == q['correct']:
                        points = 10
                        st.session_state.scores[q['type']] = min(100, st.session_state.scores[q['type']] + points)
                        st.success(f"✅ **BENAR!** +{points} poin untuk {q['type']}")
                    else:
                        st.error(f"❌ **SALAH!** Jawaban benar adalah: **{q['correct']}**")
                    
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50] + "...",
                        "type": q['type'],
                        "national": q['national'],
                        "correct": selected == q['correct'],
                        "user_answer": selected,
                        "correct_answer": q['correct'],
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
        col_chart, col_stats = st.columns([2, 1])
        with col_chart:
            df_chart = pd.DataFrame({
                "Kecerdasan": ["IQ", "EQ", "SQ", "AQ"],
                "Skor": [
                    st.session_state.scores["IQ"],
                    st.session_state.scores["EQ"],
                    st.session_state.scores["SQ"],
                    st.session_state.scores["AQ"]
                ]
            })
            st.bar_chart(df_chart.set_index("Kecerdasan"), height=300)
        with col_stats:
            st.markdown("### 📈 Statistik")
            persentase_iq = st.session_state.scores["IQ"]
            persentase_eq = st.session_state.scores["EQ"]
            persentase_sq = st.session_state.scores["SQ"]
            persentase_aq = st.session_state.scores["AQ"]
            st.markdown(f"""
            - 🧠 **IQ:** {persentase_iq}%
            - ❤️ **EQ:** {persentase_eq}%
            - 🙏 **SQ:** {persentase_sq}%
            - 💪 **AQ:** {persentase_aq}%
            """)
        st.markdown("---")
        st.markdown("### 📝 Rekomendasi Peningkatan")
        lowest = min(st.session_state.scores, key=st.session_state.scores.get)
        if st.session_state.scores[lowest] < 50:
            if lowest == "IQ":
                st.info("📚 **Tingkatkan IQ-mu:** Baca buku sejarah Indonesia, coba teka-teki silang, atau main puzzle!")
            elif lowest == "EQ":
                st.info("❤️ **Tingkatkan EQ-mu:** Latih mendengarkan orang lain, ikut kegiatan sosial, atau jurnal perasaan!")
            elif lowest == "SQ":
                st.info("🙏 **Tingkatkan SQ-mu:** Pelajari nilai-nilai Pancasila, ikut kegiatan kerohanian, atau refleksi diri!")
            else:
                st.info("💪 **Tingkatkan AQ-mu:** Tantang dirimu dengan target harian, jangan mudah menyerah, belajar dari kegagalan!")
        else:
            st.success("🌟 Luar biasa! Semua kecerdasanmu sudah terasah dengan baik. Pertahankan!")
        if st.session_state.history:
            st.markdown("---")
            st.markdown("### 📜 Riwayat Kuis (10 Terakhir)")
            history_df = pd.DataFrame(st.session_state.history[-10:])
            history_df = history_df[["timestamp", "type", "question", "correct"]]
            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
            history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil"]
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 🏆 Pencapaianmu")
        col1, col2, col3, col4 = st.columns(4)
        badges = {
            "IQ": ("🧠", "Cendekia Nusantara", 50),
            "EQ": ("❤️", "Empati Bangsa", 50),
            "SQ": ("🙏", "Bhinneka Sejati", 50),
            "AQ": ("💪", "Pejuang Tangguh", 50)
        }
        for i, (t, (icon, name, target)) in enumerate(badges.items()):
            cols = [col1, col2, col3, col4]
            with cols[i]:
                if st.session_state.scores[t] >= target:
                    st.success(f"{icon}\n**{name}**\n✅ Teraih!")
                else:
                    st.caption(f"{icon}\n{name}\n🔒 {target - st.session_state.scores[t]} poin lagi")
        st.markdown("---")
        if all(st.session_state.scores[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ"]):
            st.balloons()
            st.success("""
            ## 🎉 SELAMAT! 🎉
            ### Anda telah meraih gelar tertinggi:
            # **PAHLAWAN CERDAS NUSANTARA**
            
            Anda telah mengasah keempat kecerdasan secara seimbang!
            """)
        elif nkhm >= 60:
            st.info("## 🌟 Cendekia Muda\nTerus tingkatkan kecerdasan yang masih rendah menuju gelar Pahlawan Cerdas!")
        st.markdown("---")
        st.markdown("### 📊 Ringkasan Belajar")
        answered = len(st.session_state.history)
        correct = sum(1 for h in st.session_state.history if h["correct"])
        accuracy = (correct / answered * 100) if answered > 0 else 0
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric("📖 Total Soal", answered)
        with metric_col2:
            st.metric("✅ Benar", correct)
        with metric_col3:
            st.metric("❌ Salah", answered - correct)
        with metric_col4:
            st.metric("📊 Akurasi", f"{accuracy:.1f}%")

import streamlit as st
import time

def show_splash():
    if "splash_done" not in st.session_state:
        placeholder = st.empty()
        with placeholder.container():
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image("https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Indonesia.svg", width=150)
                st.markdown("<h1 style='text-align: center;'>🇮🇩 NKHM Nusantara</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-size: 18px;'>Asah 4 Kecerdasan + Nasionalisme</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Tim Cerdas Bangsa</p>", unsafe_allow_html=True)
                progress_bar = st.progress(0)
                for percent in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent + 1)
                st.markdown("<p style='text-align: center;'>🎮 Menggali potensi Nusantara...</p>", unsafe_allow_html=True)
        placeholder.empty()
        st.session_state.splash_done = True
        st.rerun()
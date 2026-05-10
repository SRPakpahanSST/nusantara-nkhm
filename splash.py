# splash.py
import streamlit as st

def show_splash():
    """Menampilkan splash screen dengan logo, deskripsi, dan tombol 'Mulai Sekarang'."""
    # Jika aplikasi sudah dimulai, lewati splash
    if st.session_state.get("app_started", False):
        return
    
    # Bersihkan area utama dan tampilkan splash
    splash = st.empty()
    with splash.container():
        # Layout agar tampilan di tengah
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Logo (gunakan bendera Indonesia, bisa diganti gambar sendiri)
            st.image("https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Indonesia.svg", width=150)
            st.markdown("<h1 style='text-align: center;'>🇮🇩 NKHM Nusantara</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 18px;'>Asah 4 Kecerdasan + Nasionalisme</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Tim Cerdas Bangsa</p>", unsafe_allow_html=True)
            
            st.markdown("---")
            # Deskripsi
            st.markdown("""
            <div style='text-align: center;'>
                <p>🧠 <b>IQ</b> – Kecerdasan Intelektual<br>
                ❤️ <b>EQ</b> – Kecerdasan Emosi<br>
                🙏 <b>SQ</b> – Kecerdasan Spiritual<br>
                💪 <b>AQ</b> – Kecerdasan Daya Juang</p>
                <p>Berbasis nilai-nilai kebangsaan dan sejarah Indonesia.</p>
                <p>Rumus NKHM: <b>((IQ+EQ) × (SQ+AQ)) / ((IQ+EQ)+(SQ+AQ))</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            # Tombol Mulai Sekarang
            if st.button("🚀 Mulai Sekarang", use_container_width=True):
                st.session_state.app_started = True
                st.rerun()
    
    # Hentikan eksekusi app utama sampai tombol ditekan
    st.stop()
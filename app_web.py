import streamlit as st
import google.generativeai as genai

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# PASTE KUNCI BARU LO DI DALAM TANDA KUTIP DI BAWAH INI
API_KEY = "AIzaSyDUc4winXU8_u7FEqnSaQal4q6mPCwf6SU" 
genai.configure(api_key=API_KEY)

# Memakai model flash yang paling baru dan kencang
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat agar mengalir ke atas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
# Kotak input ini akan otomatis nempel di bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI (Muncul di atas kolom input)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Jika kunci diblokir lagi karena bocor
            if "403" in str(e):
                st.error("Waduh, kuncinya mati lagi! Google deteksi bocor. Buat baru lagi ya.")
            else:
                st.error(f"Error: {e}")

# --- 5. SIDEBAR ---
with st.sidebar:
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

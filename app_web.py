import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# Menggunakan API Key lo yang sudah terbukti valid
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# JURUS ANTI-ERROR 404: Cari model otomatis
@st.cache_resource
def get_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(models[0])
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama agar mengalir ke atas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    # Simpan dan tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # JAWABAN AI
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                # Kasih jeda dikit biar server gak kaget (Anti-Error 429)
                time.sleep(1) 
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.error("Server lagi penuh Bro, tunggu 1 menit ya! Jangan spam chatnya.")
                elif "403" in str(e):
                    st.error("Kuncinya diblokir karena bocor! Jangan diposting di chat publik lagi.")
                else:
                    st.error(f"Eror: {e}")

# --- 5. SIDEBAR ---
with st.sidebar:
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

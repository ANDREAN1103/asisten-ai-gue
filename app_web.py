import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY LANGSUNG ---
# Ganti teks di bawah dengan API Key asli lo
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# JURUS OTOMATIS: Mencari model yang tersedia biar gak Error 404
@st.cache_resource
def get_model():
    try:
        # Nanya ke Google model apa yang aktif buat akun lo
        active_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(active_models[0])
    except:
        # Cadangan jika pencarian otomatis gagal
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                # Memanggil jawaban AI
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.error("Server penuh! Google membatasi akun gratis. Tunggu 1-2 menit ya.")
                else:
                    st.error(f"Kendala teknis: {e}")

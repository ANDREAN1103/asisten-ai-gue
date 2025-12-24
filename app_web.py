import streamlit as st
import google.generativeai as genai

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# HAPUS teks di bawah ini dan PASTE kunci baru lo di dalam tanda kutip!
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# JURUS SAPU JAGAT: Nyari model otomatis biar gak Error 404
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

# Nampilin riwayat chat biar numpuk ke atas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    # Simpan dan tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # JAWABAN AI (Muncul di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                # INI BARIS PENTING: Mengirim pertanyaan ke Google
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "400" in str(e):
                    st.error("API Key salah salin Bro! Coba cek lagi kuncinya.")
                elif "403" in str(e):
                    st.error("Kuncinya diblokir (bocor)! Buat baru lagi ya.")
                else:
                    st.error(f"Eror: {e}")

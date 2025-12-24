import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY LANGSUNG ---
# HAPUS tulisan di bawah dan PASTE API Key lo di dalam tanda kutip!
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# JURUS OTOMATIS: Biar gak kena Error 404 (Nyari model yang aktif sendiri)
@st.cache_resource
def get_working_model():
    try:
        # Nanya ke Google model apa yang bisa dipake akun Andrean
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(models[0])
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_working_model()

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
                    st.error("Server penuh! Tunggu 1 menit ya.")
                elif "400" in str(e):
                    st.error("API Key lo salah ketik atau nggak valid, Bro!")
                else:
                    st.error(f"Eror: {e}")

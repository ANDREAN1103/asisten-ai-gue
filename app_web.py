import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", page_icon="🤖", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# GANTI "MASUKKAN_KUNCI_BARU_LO" dengan API Key yang baru lo buat!
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8" 
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    # Nyari model otomatis biar gak kena error 404 lagi
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(models[0])
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Nampilin chat lama biar jawaban AI selalu di atas input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🚀 Info Bot")
    st.write("Dibuat oleh: **ANDREAN**")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. KOLOM TANYA (DI BAWAH) ---
# Kotak input ini bakal nempel di bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Kendala: {e}")

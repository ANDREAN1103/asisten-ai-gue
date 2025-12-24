import streamlit as st
import google.generativeai as genai

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Bot", page_icon="🤖", layout="centered")

# --- SIDEBAR (INFO PEMBUAT) ---
with st.sidebar:
    st.title("🚀 Info Bot")
    st.write("Dibuat oleh: **ANDREAN**")
    st.divider()
    st.write("AI ini sudah online 24 jam!")

st.title("🤖 Chatbot AI BY : ANDREAN")
st.caption("Tanya apa aja, gue siap bantu!")

# --- SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    # JURUS OTOMATIS: Biar gak error 404 lagi
    model_aktif = "gemini-pro" # Coba pake nama standar dulu
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_aktif = m.name
                break
    except:
        model_aktif = "models/gemini-1.5-flash" # Backup kalau list gagal

    return genai.GenerativeModel(model_name=model_aktif)
model = get_model()

# --- LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})


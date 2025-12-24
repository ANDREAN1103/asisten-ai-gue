import streamlit as st
import google.generativeai as genai

# Setup Tampilan Web
st.set_page_config(page_title="AI Chatbot Gue", page_icon="🤖")
st.title("🤖 Chatbot AI BY : ANDREAN")

# Masukkan API Key lo
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

# JURUS OTOMATIS: Biar gak error 404 lagi
@st.cache_resource
def get_model():
    model_aktif = ""
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_aktif = m.name
            break
    return genai.GenerativeModel(model_name=model_aktif)

model = get_model()

# Inisialisasi kotak chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Chat
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gunakan penanganan error yang lebih detail
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Duh, ada masalah teknis: {e}")
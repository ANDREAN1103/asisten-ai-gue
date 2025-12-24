import streamlit as st
import google.generativeai as genai

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# API Key dari gambar terakhir lo udah bener, pake yang itu aja
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# Memakai model 'pro' karena 'flash' lo lagi limit (Error 429)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 3. RIWAYAT CHAT ---
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
        with st.spinner("Lagi mikir pake server cadangan..."):
            try:
                # Memanggil jawaban AI
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.error("Server Google lagi sibuk banget, Bro! Coba lagi dalam 30 detik ya.")
                else:
                    st.error(f"Eror teknis: {e}")

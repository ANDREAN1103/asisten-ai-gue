import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY LANGSUNG ---
# PASTE API Key lo di bawah ini (Pastiin gak ada spasi tambahan)
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# JURUS ANTI-SERVER PENUH: Coba beberapa model sekaligus
def dapatkan_respon(prompt_user):
    # Daftar model dari yang paling pinter sampe yang paling ringan
    daftar_model = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b']
    
    for nama_model in daftar_model:
        try:
            model = genai.GenerativeModel(nama_model)
            return model.generate_content(prompt_user).text
        except Exception as e:
            # Kalau error 429 (Penuh), dia bakal lanjut nyoba model berikutnya
            if "429" in str(e):
                continue
            else:
                return f"Ada kendala teknis: {e}"
    
    return "Waduh Bro, semua server Google lagi penuh banget! Coba lagi 1 menit lagi ya."

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
        with st.spinner("Lagi nyari server yang kosong..."):
            jawaban = dapatkan_respon(prompt)
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})

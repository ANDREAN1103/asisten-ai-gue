import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. KONEKSI KE SECRETS ---
try:
    # Baris ini bakal ngambil API_KEY yang lo tulis di menu Secrets tadi
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Waduh Bro, API_KEY belum kebaca di Secrets Streamlit. Cek lagi ya!")
    st.stop()

# Pilih model yang paling stabil
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. TAMPILAN JAWABAN (DI ATAS) ---
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
        try:
            # Kirim pesan ke AI
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.error("Server Google lagi penuh, Bro! Tunggu 1 menit baru chat lagi ya.")
            else:
                st.error(f"Eror: {e}")

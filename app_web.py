import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", page_icon="🤖", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Andrean AI v5.0")
    st.write("Dibuat oleh: **ANDREAN**")
    st.divider()
    st.info("Gunakan tombol + di samping kolom chat untuk menu tambahan!")

st.title("🤖 Chatbot AI BY : ANDREAN")

# --- SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- INISIALISASI PESAN ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- TAMPILKAN CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- BAGIAN BAWAH (MENU + & INPUT CHAT) ---
# Kita buat container biar posisinya tetap di bawah (sticky)
container = st.container()

with container:
    # Trik kolom biar sejajar di bawah
    col1, col2 = st.columns([0.15, 0.85])
    
    with col1:
        # Tombol Popover (Menu Alat)
        with st.popover("➕"):
            st.write("### 🛠️ Menu Alat")
            uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])
            if st.button("🗑️ Hapus Chat"):
                st.session_state.messages = []
                st.rerun()
    
    with col2:
        prompt = st.chat_input("Tanya apa aja, Bro...")

# --- LOGIKA PENGIRIMAN ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if 'uploaded_file' in locals() and uploaded_file:
            img = Image.open(uploaded_file)
            response = model.generate_content([prompt, img])
            st.image(img, width=250)
        else:
            response = model.generate_content(prompt)
            
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

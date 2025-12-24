import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", page_icon="🤖", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Andrean AI v4.0")
    st.write("Dibuat oleh: **ANDREAN**")
    st.divider()
    st.info("Klik tombol + di bawah buat menu tambahan!")

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

# --- MENU "+" (POPOVER) ---
# Kita taro menu ini tepat di atas input chat biar estetik
col1, col2 = st.columns([0.1, 0.9])

with col1:
    with st.popover("➕"):
        st.write("### Menu Alat")
        uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])
        if st.button("Hapus Semua Chat"):
            st.session_state.messages = []
            st.rerun()

# --- INPUT CHAT ---
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Logika analisis gambar kalau ada file di-upload
        if uploaded_file:
            img = Image.open(uploaded_file)
            response = model.generate_content([prompt, img])
            st.image(img, width=300)
        else:
            response = model.generate_content(prompt)
            
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

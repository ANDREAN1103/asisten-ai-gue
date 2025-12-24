import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Super", page_icon="🚀", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Andrean AI v2.0")
    st.write("Sekarang gue bisa LIAT FOTO lo, Bro!")
    st.divider()
    st.write("Dibuat oleh: **ANDREAN**")

st.title("🤖 Chatbot AI BY : ANDREAN")
st.caption("Kirim teks atau upload foto, gue jabanin!")

# --- SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- FITUR UPLOAD GAMBAR ---
uploaded_file = st.file_uploader("Pilih foto buat dianalisis...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto yang lo upload", use_container_width=True)

# --- LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya sesuatu tentang fotonya atau chat biasa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        # Jika ada gambar, kirim gambar + teks ke AI
        if uploaded_file:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
            
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Ultra", page_icon="🤖", layout="centered")

st.title("🤖 Chatbot AI BY : ANDREAN")

# --- SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- RIWAYAT CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama di atas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=250)

# --- AREA INPUT BAWAH (BARIS TUNGGAL) ---
# Gunakan container biar dia nempel di bawah
with st.container():
    # Buat dua kolom: Kolom Kecil (Menu +) dan Kolom Besar (Input Chat)
    # Perbandingan 0.15 dan 0.85 biar sejajar pas
    col_menu, col_chat = st.columns([0.15, 0.85])
    
    with col_menu:
        # Tombol + yang berisi menu Alat
        with st.popover("➕"):
            st.write("### 🛠️ Alat")
            up_file = st.file_uploader("Kirim Foto", type=["jpg", "png", "jpeg"])
            if st.button("🗑️ Reset"):
                st.session_state.messages = []
                st.rerun()
    
    with col_chat:
        # Input chat ditaruh di sini biar sejajar sama tombol +
        prompt = st.chat_input("Tanya apa aja, Bro...")

# --- LOGIKA PENGIRIMAN ---
if prompt:
    user_payload = {"role": "user", "content": prompt}
    
    img_data = None
    if up_file:
        img_data = Image.open(up_file)
        user_payload["image"] = img_data
    
    st.session_state.messages.append(user_payload)
    
    # Jalankan respon AI
    with st.chat_message("user"):
        st.markdown(prompt)
        if img_data: st.image(img_data, width=250)

    with st.chat_message("assistant"):
        if img_data:
            response = model.generate_content([prompt, img_data])
        else:
            response = model.generate_content(prompt)
            
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

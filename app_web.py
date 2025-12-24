import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", page_icon="🤖", layout="centered")

# --- JUDUL ---
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- RIWAYAT CHAT (DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat agar jawaban AI selalu di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=250)

# --- MENU ALAT (SIDEBAR) ---
with st.sidebar:
    st.title("🛠️ Menu Alat")
    up_file = st.file_uploader("Kirim Foto", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- KOLOM TANYA (DI BAWAH) ---
# st.chat_input otomatis akan selalu berada di posisi paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # 1. Simpan pesan user
    user_payload = {"role": "user", "content": prompt}
    img_data = None
    
    # Cek jika ada file yang diupload (Mencegah error image_56f006.png)
    if up_file:
        img_data = Image.open(up_file)
        user_payload["image"] = img_data
    
    st.session_state.messages.append(user_payload)
    
    # 2. Tampilkan pesan user segera
    with st.chat_message("user"):
        st.markdown(prompt)
        if img_data:
            st.image(img_data, width=250)

    # 3. Jawaban AI (Muncul di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                if img_data:
                    response = model.generate_content([prompt, img_data])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Waduh Bro, ada masalah teknis: {e}")

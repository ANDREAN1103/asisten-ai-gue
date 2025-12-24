import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Modern", page_icon="🤖", layout="centered")

# --- JUDUL ---
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

# --- 1. TAMPILKAN JAWABAN DI ATAS ---
# Bagian ini akan otomatis scroll ke atas saat ada chat baru
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=250)

# --- 2. KOLOM BERTANYA DI BAWAH (PERSIS REQUEST LO) ---
# Di Streamlit, st.chat_input otomatis nempel di bawah layar
prompt = st.chat_input("Tanya apa aja, Bro...")

# Tombol Tambahan (+) buat Upload Gambar (Opsional di Sidebar biar rapi)
with st.sidebar:
    st.title("🛠️ Menu Alat")
    up_file = st.file_uploader("Kirim Foto", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- LOGIKA PROSES ---
if prompt:
    user_payload = {"role": "user", "content": prompt}
    
    img_data = None
    if up_file:
        img_data = Image.open(up_file)
        user_payload["image"] = img_data
    
    # Simpan ke memori
    st.session_state.messages.append(user_payload)
    
    # Munculkan pesan user di atas
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
            if img_data: st.image(img_data, width=250)

        # Munculkan jawaban AI di atas kolom input
        with st.chat_message("assistant"):
            with st.spinner("Lagi mikir..."):
                if img_data:
                    response = model.generate_content([prompt, img_data])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

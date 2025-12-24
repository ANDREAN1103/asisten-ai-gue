import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", page_icon="🤖", layout="centered")

st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

# JURUS SAPU JAGAT: Nyari model yang idup otomatis
@st.cache_resource
def get_working_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Pilih model pertama yang tersedia (biasanya yang paling stabil)
        return genai.GenerativeModel(models[0])
    except:
        # Jika gagal list, paksa pake jalur alternatif
        return genai.GenerativeModel('models/gemini-1.5-flash-latest')

model = get_working_model()

# --- RIWAYAT CHAT (DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

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
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    user_payload = {"role": "user", "content": prompt}
    img_data = None
    if up_file:
        img_data = Image.open(up_file)
        user_payload["image"] = img_data
    
    st.session_state.messages.append(user_payload)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if img_data:
            st.image(img_data, width=250)

    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                if img_data:
                    # Gunakan model yang sama untuk gambar
                    response = model.generate_content([prompt, img_data])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Menampilkan pesan error yang lebih jelas buat kita debug
                st.error(f"Masih ada kendala teknis: {e}")

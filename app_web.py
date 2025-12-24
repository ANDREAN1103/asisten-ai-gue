import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Ultra", page_icon="🤖", layout="centered")

# CSS biar tampilan chat makin bersih
st.markdown("""<style> .stChatMessage { border-radius: 15px; } </style>""", unsafe_allow_html=True)

st.title("🤖 Chatbot AI BY : ANDREAN")

# --- 2. SETUP API KEY (Ganti dengan kunci asli lo) ---
# Masukkan API Key lo di sini. Kalau punya lebih dari satu, ganti kodenya nanti.
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    # Menggunakan model paling stabil untuk menghindari error 404
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama agar jawaban AI selalu berada di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=250)

# --- 4. MENU ALAT (SIDEBAR) ---
with st.sidebar:
    st.title("🛠️ Menu Alat")
    # Fitur kirim foto lewat sidebar biar area chat utama bersih
    up_file = st.file_uploader("Kirim Foto", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. KOLOM TANYA (DI BAWAH) ---
# Fungsi ini otomatis mengunci kolom input di bagian paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan pesan user ke riwayat
    user_payload = {"role": "user", "content": prompt}
    img_data = None
    
    if up_file:
        img_data = Image.open(up_file)
        user_payload["image"] = img_data
    
    st.session_state.messages.append(user_payload)
    
    # Tampilkan pesan user di area chat
    with st.chat_message("user"):
        st.markdown(prompt)
        if img_data:
            st.image(img_data, width=250)

    # Jalankan respon AI (Akan muncul tepat di atas kolom input)
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
                # Menangkap error seperti PermissionDenied atau QuotaExceeded
                st.error(f"Waduh Bro, ada kendala: {e}")

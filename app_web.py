import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Ultra", page_icon="🤖", layout="centered")

# --- CSS CUSTOM: Bikin kotak chat ala Gemini ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stVerticalBlock"] > div:has(div.stPopover) {
        background-color: #1e1e1e;
        border-radius: 25px;
        padding: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Andrean AI v7.0")
    st.write("Dibuat oleh: **ANDREAN**")
    st.divider()
    st.info("Upload foto via menu + lalu ketik pesan untuk kirim bareng!")

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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=250)

# --- KOTAK INPUT BAWAH (PERSIS TANDA MERAH LO) ---
with st.container():
    # Baris menu Alat dan Plus
    c1, c2, c3 = st.columns([0.1, 0.2, 0.7])
    with c1:
        with st.popover("➕"):
            up_file = st.file_uploader("Kirim Foto", type=["jpg", "png", "jpeg"])
    with c2:
        st.write("🛠️ Alat") # Menandakan menu alat aktif
    
    # Input chat tetap di paling bawah
    prompt = st.chat_input("Tanya apa aja, Bro...")

# --- LOGIKA PROSES ---
if prompt:
    user_payload = {"role": "user", "content": prompt}
    
    # Ambil gambar kalau ada yang di-upload
    img_data = None
    if up_file:
        img_data = Image.open(up_file)
        user_payload["image"] = img_data
    
    st.session_state.messages.append(user_payload)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if img_data: st.image(img_data, width=250)

    with st.chat_message("assistant"):
        with st.spinner("Sabar Bro, lagi mikir..."):
            if img_data:
                response = model.generate_content([prompt, img_data])
            else:
                response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

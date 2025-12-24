import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", page_icon="🤖", layout="centered")

# Judul di tengah
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# Pastikan API Key ini aktif ya, Bro!
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    # Menggunakan model paling stabil khusus teks
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama agar jawaban AI selalu berada di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SIDEBAR UNTUK INFO & RESET ---
with st.sidebar:
    st.title("🚀 Info Bot")
    st.write("Dibuat oleh: **ANDREAN**")
    st.divider()
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. KOLOM TANYA (DI BAWAH) ---
# st.chat_input otomatis akan selalu berada di posisi paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan dan tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jalankan respon AI (Akan muncul tepat di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Menampilkan error jika kuota habis atau API bermasalah
                if "429" in str(e):
                    st.error("Kuota gratisan habis Bro, tunggu 1 menit ya!")
                else:
                    st.error(f"Ada kendala teknis: {e}")

import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Pro", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# Langsung gue pasang kunci baru lo di sini
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8" 
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    # Pake model flash-latest biar gak gampang eror 404
    return genai.GenerativeModel('gemini-1.5-flash-latest')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama agar jawaban AI selalu di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🚀 Andrean AI")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. KOLOM TANYA (DI BAWAH) ---
# Fungsi st.chat_input otomatis bikin kotak tanya nempel di bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan dan tampilin pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jalankan respon AI (Jawaban muncul di atas kolom input)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "403" in str(e):
                st.error("Waduh, kuncinya diblokir lagi! Jangan diposting di chat publik ya, Bro.")
            elif "429" in str(e):
                st.error("Sabar, limit gratisan habis. Tunggu 1 menit!")
            else:
                st.error(f"Eror: {e}")

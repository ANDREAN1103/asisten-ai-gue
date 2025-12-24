import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", page_icon="🤖", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# Masukkan API Key terbaru lo di sini
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8" 
genai.configure(api_key=API_KEY)

# JURUS ANTI-ERROR 404: Mencari model yang tersedia secara otomatis
@st.cache_resource
def get_working_model():
    try:
        # Mengambil daftar model yang aktif di akun lo
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Menggunakan model pertama yang ditemukan (biasanya gemini-1.5-flash atau gemini-pro)
        return genai.GenerativeModel(available_models[0])
    except Exception:
        # Jika gagal otomatis, gunakan fallback yang paling umum
        return genai.GenerativeModel('gemini-pro')

model = get_working_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama agar riwayat mengalir di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
# st.chat_input otomatis akan selalu berada di posisi paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan dan tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jalankan respon AI (Jawaban akan muncul tepat di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Menangkap error limit (429) atau error lainnya
                if "429" in str(e):
                    st.error("Sabar Bro, kuota gratisan habis. Tunggu 1 menit ya!")
                else:
                    st.error(f"Ada kendala teknis: {e}")

# --- 5. SIDEBAR UNTUK RESET ---
with st.sidebar:
    st.title("🚀 Andrean AI")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

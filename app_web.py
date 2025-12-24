import streamlit as st
import google.generativeai as genai

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# API Key baru lo udah gue pasang di sini sesuai gambar
API_KEY = "AIzaSyDUc4winXU8_u7FEqNSaQal4q6mPCwf6SU" 
genai.configure(api_key=API_KEY)

# JURUS ANTI-ERROR 404: Nyari model yang tersedia secara otomatis
@st.cache_resource
def get_model():
    try:
        # Mencari daftar model yang aktif di akun lo
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(available_models[0])
    except:
        # Jika gagal otomatis, gunakan model standar
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama agar riwayat mengalir di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
# st.chat_input otomatis nempel di bagian paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan dan tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jalankan respon AI (Jawaban akan muncul tepat di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                # INI BAGIAN YANG TADI SALAH: Memanggil AI untuk menjawab
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Menampilkan pesan error yang lebih jelas
                if "429" in str(e):
                    st.error("Kuota habis, tunggu 1 menit ya!")
                elif "403" in str(e):
                    st.error("Waduh, kuncinya diblokir lagi! Jangan diposting di chat publik.")
                else:
                    st.error(f"Ada kendala teknis: {e}")

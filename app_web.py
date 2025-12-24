import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# API Key yang lo pake di gambar sebelumnya udah bener, pake itu lagi
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg" 
genai.configure(api_key=API_KEY)

# JURUS PAMUNGKAS: Cari model yang tersedia secara otomatis biar gak 404
@st.cache_resource
def get_working_model():
    try:
        # Ambil daftar model yang aktif di akun lo
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Pake model pertama yang ketemu (biasanya flash atau pro)
        return genai.GenerativeModel(models[0])
    except Exception:
        # Fallback kalau cara otomatis gagal
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_working_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama agar riwayat mengalir di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
# st.chat_input akan otomatis nempel di bagian paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan dan tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jalankan respon AI (Akan muncul tepat di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                # Memanggil AI untuk menjawab
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Nangkep eror limit kuota (429) atau kunci bocor (403)
                if "429" in str(e):
                    st.error("Server lagi penuh Bro, tunggu 1 menit ya!")
                elif "403" in str(e):
                    st.error("Kuncinya diblokir (bocor)! Ganti kunci baru di AI Studio.")
                else:
                    st.error(f"Ada kendala teknis: {e}")

# --- 5. SIDEBAR ---
with st.sidebar:
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

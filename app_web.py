import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Stabil", page_icon="🤖", layout="centered")

st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
API_KEY = "AIzaSyAs2eRiuYGkitmNYqj_HvIhsrQrqWbIIy8"
genai.configure(api_key=API_KEY)

# JURUS ANTI-ERROR: Nyari nama model yang bener secara otomatis
@st.cache_resource
def get_working_model():
    try:
        # Nyari daftar model yang support chat
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Pake model pertama yang ketemu (biasanya gemini-pro atau flash)
        return genai.GenerativeModel(models[0])
    except:
        # Kalau gagal nyari, paksa pake nama paling umum
        return genai.GenerativeModel('gemini-pro')

model = get_working_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Nampilin chat biar jawaban AI selalu di atas kolom input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🚀 Info Bot")
    st.write("Dibuat oleh: **ANDREAN**")
    st.divider()
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. KOLOM TANYA (DI BAWAH) ---
# st.chat_input otomatis nempel di bagian paling bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    
    # Simpan dan tampilin pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jalankan respon AI
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Nangkep error kuota (429) atau error lainnya
                if "429" in str(e):
                    st.error("Kuota gratis habis Bro, tunggu 1 menit ya!")
                else:
                    st.error(f"Ada kendala teknis: {e}")

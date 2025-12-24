import streamlit as st
import google.generativeai as genai

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. SETUP API KEY ---
# PASTE KUNCI BARU YANG BARU LO BUAT DI SINI!
API_KEY = "AIzaSyDUc4winXU8_u7FEqnSaQal4q6mPCwf6SU" 
genai.configure(api_key=API_KEY)

# JURUS SAPU JAGAT: Nyari model otomatis biar gak Error 404
@st.cache_resource
def get_model():
    try:
        # Minta Google kasih daftar model yang aktif
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(models[0])
    except:
        # Kalau gagal, pake cadangan nama yang paling umum
        return genai.GenerativeModel('gemini-pro')

model = get_model()

# --- 3. RIWAYAT CHAT (JAWABAN DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Nampilin chat biar riwayatnya numpuk ke atas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
# Kotak input ini dijamin nempel di bawah layar
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jawaban AI (Muncul di atas kolom input)
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Nangkep error 403 (bocor) atau 429 (limit)
                if "403" in str(e):
                    st.error("Kuncinya diblokir lagi! Jangan diposting di sini ya Bro.")
                elif "429" in str(e):
                    st.error("Limit habis, tunggu 1 menit.")
                else:
                    st.error(f"Eror: {e}")

# --- 5. SIDEBAR ---
with st.sidebar:
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()


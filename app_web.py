import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="Andrean AI Chat", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot AI BY : ANDREAN</h2>", unsafe_allow_html=True)

# --- 2. KONEKSI KE SECRETS (YANG UDAH LO PASANG) ---
try:
    # Baris ini bakal narik API_KEY dari menu Secrets yang lo isi tadi
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Waduh, API_KEY di menu Secrets belum kebaca! Cek lagi tulisannya.")
    st.stop()

# JURUS OTOMATIS: Biar gak kena Error 404 lagi
@st.cache_resource
def get_auto_model():
    try:
        # Nanya ke Google: "Model apa yang aktif di akun Andrean?"
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Pake model pertama yang dia kasih (pasti ada)
        return genai.GenerativeModel(models[0])
    except:
        # Cadangan terakhir kalo Google lagi pelit
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_auto_model()

# --- 3. TAMPILAN JAWABAN (DI ATAS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOLOM TANYA (DI BAWAH) ---
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Kirim pesan ke model otomatis tadi
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.error("Server penuh! Tunggu 1 menit ya.")
            else:
                st.error(f"Eror: {e}")

import streamlit as st
import google.generativeai as genai
import time

# --- 1. SETUP TAMPILAN ---
st.set_page_config(page_title="AI Chatbot Gue", page_icon="🤖")
st.title("🤖 Chatbot AI BY : ANDREAN")

# --- 2. MASUKKAN API KEY LANGSUNG ---
# Gue pake kunci yang lo pake di VSC tadi
API_KEY = "AIzaSyC-Rsgzx2eXhCBZpzOleycWA1_CtbxBUIg"
genai.configure(api_key=API_KEY)

# --- 3. JURUS OTOMATIS CARI MODEL ---
@st.cache_resource
def get_model():
    try:
        # Nyari model yang beneran aktif di akun lo
        active_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(active_models[0])
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 4. RIWAYAT CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. INPUT CHAT ---
if prompt := st.chat_input("Tanya apa aja, Bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # JURUS ANTI-429 (Mencoba 3 kali kalau server penuh)
        for i in range(3):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                break
            except Exception as e:
                if "429" in str(e) and i < 2:
                    placeholder.warning(f"Server penuh, nyoba lagi dalam {i+2} detik...")
                    time.sleep(i + 2)
                else:
                    full_response = f"Aduh Bro, server beneran lagi mogok. Error: {e}"
        
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

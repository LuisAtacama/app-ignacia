import streamlit as st
import random
from openai import OpenAI

# 1. CONFIGURACIÓN (Debe ser lo primero)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. FUNCIÓN PARA LEER SUS TEXTOS
def leer_archivo(nombre, backup):
    try:
        with open(nombre, "r", encoding="utf-8") as f:
            if nombre == "adn.txt": return f.read()
            return [line.strip() for line in f.readlines() if line.strip()]
    except: return backup

# Cargamos sus archivos desde GitHub
APODOS = leer_archivo("senoras.txt", ["Loquita", "Molita", "Ignacita"])
CHISTES = leer_archivo("chistes.txt", ["¿Qué le dice un pan a otro pan? Te presento a una miga."])
ADN_SISTEMA = leer_archivo("adn.txt", "Eres el papá de Ignacita. Habla con amor.")

# 3. LÓGICA DE NAVEGACIÓN (Persistente)
if "entrado" not in st.session_state:
    st.session_state.entrado = False

# 4. PORTADA (Solo si no ha entrado)
if not st.session_state.entrado:
    st.markdown("""
    <style>
        .portada { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; display: flex; align-items: center; justify-content: center; z-index: 999; }
        .logo { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
        .stButton > button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: transparent !important; border: none !important; color: transparent !important; z-index: 9999 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="portada"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo"></div>', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="portada_btn"):
        st.session_state.entrado = True
        st.session_state.nombre_saludo = random.choice(APODOS)
        st.rerun()

# 5. INTERIOR (Solo si ya entró)
else:
    st.markdown("""
    <style>
        .stApp { background-color: white; }
        .stButton > button { position: relative !important; width: 100% !important; height: auto !important; z-index: 1 !important; background-color: #f0f2f6 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title(f"❤️ ¡Hola, mi {st.session_state.nombre_saludo}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # WhatsApp
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:15px;display:block;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="chiste"):
        st.info(random.choice(CHISTES))

    st.divider()
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    for m in st.session_state.mensajes:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.mensajes.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_SISTEMA}] + st.session_state.mensajes
            )
            r = res.choices[0].message.content
        except:
            r = "Pucha mi amor, se me cortó la señal..."
        with st.chat_message("assistant"):
            st.markdown(r)
        st.session_state.mensajes.append({"role": "assistant", "content": r})

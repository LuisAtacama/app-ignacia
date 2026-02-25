import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN (Debe ir al principio)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. FUNCIÓN DE LECTURA LIMPIA
def leer_archivo_limpio(nombre, es_adn=False):
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
                # Limpieza de caracteres invisibles
                for r in ['Ñ', 'ï»¿', 'Â', '\ufffd']:
                    texto = texto.replace(r, '')
                if es_adn: return texto.strip()
                return [line.strip() for line in texto.split('\n') if line.strip()]
    except: pass
    return "Eres Luis, el papá de Ignacita." if es_adn else ["Ignacita"]

# Carga de datos
ADN_SISTEMA = leer_archivo_limpio("adn.txt", es_adn=True)
APODOS = leer_archivo_limpio("senoras.txt")
LISTA_CHISTES = leer_archivo_limpio("chistes.txt")

# 3. LÓGICA DE NAVEGACIÓN
if "entrado" not in st.session_state:
    st.session_state.entrado = False

# --- PANTALLA DE PORTADA ---
if not st.session_state.entrado:
    # Estilo para que la portada ocupe todo
    st.markdown("""
        <style>
        .stApp { background-color: black; }
        .portada-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; }
        .logo-img { width: 80%; max-width: 400px; margin-top: -50px; }
        </style>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.image("https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif", use_container_width=True)
        st.markdown('<div style="text-align:center"><img src="https://i.postimg.cc/Bb71JpGr/image.png" style="width:70%"></div>', unsafe_allow_html=True)
        
        st.write("") # Espacio
        if st.button("✨ ENTRAR AL MUNDO DE PAAPI ✨", use_container_width=True):
            st.session_state.entrado = True
            st.session_state.nombre = random.choice(APODOS)
            st.rerun()

# --- INTERIOR DE LA APP ---
else:
    st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)
    st.title(f"❤️ ¡Hola, mi {st.session_state.nombre}!")
    
    # Imagen principal
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # Botón WhatsApp
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:20px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    # Botón Chistes
    if st.button("🤡 ¡Papi, cuéntame un chiste!", use_container_width=True):
        st.info(random.choice(LISTA_CHISTES))

    st.divider()
    
    # Chat
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_SISTEMA}] + st.session_state.chat
            )
            r = res.choices[0].message.content
        except: r = "Pucha mi amor, se cortó la señal, pero pAAPi te adora."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

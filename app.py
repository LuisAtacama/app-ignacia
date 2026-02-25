import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. FUNCIÓN ESCUDO (Limpia ruidos de texto automáticamente)
def leer_archivo_limpio(nombre, es_adn=False):
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
                # BORRADO AUTOMÁTICO DE RUIDO (La Ñ fantasma y otros)
                ruido = ['Ñ', 'ï»¿', 'Â', '\ufffd']
                for r in ruido:
                    texto = texto.replace(r, '')
                
                if es_adn: return texto.strip()
                return [line.strip() for line in texto.split('\n') if line.strip()]
    except: pass
    return "Eres Luis, el papá de Ignacita." if es_adn else ["Ignacita", "Loquita"]

# CARGA DE DATOS SEGUROS
ADN_SISTEMA = leer_archivo_limpio("adn.txt", es_adn=True)
APODOS = leer_archivo_limpio("senoras.txt")
LISTA_CHISTES = leer_archivo_limpio("chistes.txt")

# 3. NAVEGACIÓN
if "entrado" not in st.session_state: st.session_state.entrado = False

if not st.session_state.entrado:
    st.markdown("""
    <style>
        .portada { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; display: flex; align-items: center; justify-content: center; z-index: 999; }
        .logo { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
        .btn-portada > button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: transparent !important; border: none !important; color: transparent !important; z-index: 9999 !important; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="portada"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo"></div>', unsafe_allow_html=True)
    if st.button("ENTRAR", key="gate"):
        st.session_state.entrado = True
        st.session_state.nombre = random.choice(APODOS)
        st.rerun()
else:
    # --- INTERIOR ---
    st.markdown("<style>.stApp { background-color: white; } .stButton > button { position: relative !important; width: 100% !important; z-index: 1 !important; }</style>", unsafe_allow_html=True)
    st.title(f"❤️ ¡Hola, mi {st.session_state.nombre}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:15px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    if st.button("🤡 ¡Papi, chiste!", key="joke"):
        st.info(random.choice(LISTA_CHISTES))

    st.divider()
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": ADN_SISTEMA}] + st.session_state.chat)
            r = res.choices[0].message.content
        except: r = "Pucha mi amor, se cortó la señal..."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

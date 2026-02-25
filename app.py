import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. FUNCIÓN ESCUDO
def leer_archivo_limpio(nombre, es_adn=False):
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
                ruido = ['Ñ', 'ï»¿', 'Â', '\ufffd']
                for r in ruido:
                    texto = texto.replace(r, '')
                if es_adn: return texto.strip()
                return [line.strip() for line in texto.split('\n') if line.strip()]
    except: pass
    return "Eres Luis, el papá de Ignacita." if es_adn else ["Ignacita", "Loquita"]

ADN_SISTEMA = leer_archivo_limpio("adn.txt", es_adn=True)
APODOS = leer_archivo_limpio("senoras.txt")
LISTA_CHISTES = leer_archivo_limpio("chistes.txt")

# 3. NAVEGACIÓN
if "entrado" not in st.session_state: 
    st.session_state.entrado = False

# --- PORTADA ---
if not st.session_state.entrado:
    st.markdown("""
    <style>
        /* El botón ahora es una capa invisible que cubre TODO y está al frente */
        .stButton > button {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: transparent !important;
            border: none !important;
            color: transparent !important;
            z-index: 99999 !important; /* El número más alto para estar al frente */
            cursor: pointer !important;
        }
        .portada-full {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: black;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .logo-portada {
            position: absolute;
            width: 80%;
            max-width: 500px;
            z-index: 1001;
        }
    </style>
    <div class="portada-full">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-portada">
    </div>
    """, unsafe_allow_html=True)

    if st.button("ENTRAR", key="boton_maestro"):
        st.session_state.entrado = True
        st.session_state.nombre = random.choice(APODOS)
        st.rerun()

# --- INTERIOR ---
else:
    st.markdown

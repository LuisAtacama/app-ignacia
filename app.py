import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS: Aseguramos que el botón de entrada esté al frente de todo (z-index alto)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-contenedor {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 10;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 20; pointer-events: none; }
    
    /* El botón de entrar ahora es una capa superior total */
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 100; cursor: pointer;
    }
    
    /* Estilo para botones internos una vez dentro */
    .boton-real button {
        position: relative !important; width: 100% !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
        z-index: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. MOTOR DE CARGA
def cargar_datos_viva_voz():
    senoras, chistes, adn, error = [], [], "", None
    try:
        base_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        base_url = base_url.split('/edit')[0]
        if not base_url.endswith("/"): base_url += "/"
        
        url_s = f"{base_url}export?format=csv&sheet=Senoras"
        url_ch = f"{base_url}export?format=csv&sheet=Chistes"
        url_adn = f"{base_url}export?format=csv&sheet=Contexto"

        df_s = pd.read_csv(url_s)
        senoras = df_

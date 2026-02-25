import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS: Portada negra y botón invisible que cubre el 100% de la pantalla
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    
    /* El botón invisible: cubre toda la pantalla y está por ENCIMA de todo */
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999; cursor: pointer;
    }
    
    /* Estilo para los botones una vez dentro de la app */
    .boton-interno button {
        position: relative !important; width: 100% !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
        z-index: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. MOTOR DE CARGA (CSV DIRECTO PARA EVITAR ERROR 400)
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
        senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()

        df_ch = pd.read_csv(url_ch)
        chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()

        df_adn = pd.read_csv(url_adn)
        adn = "\\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
    except Exception as e:
        error = str(e)
    
    if not senoras:
        senoras = ["Señora (Sin Conexión)"]
        chistes = ["El Drive no respondió."]
        adn = "Eres Luis, el papá de Ignacita. Habla de USTED."
    return senoras, chistes, adn, error

if "DATOS" not in st.session_state:
    s, ch, adn, err = cargar_datos_viva_voz()
    st.session_state.DATOS = {"s": s, "ch": ch, "adn":

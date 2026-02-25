import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN (Inmediata y obligatoria)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. DISEÑO CSS (Portada negra y botones internos)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    
    /* Botón invisible de portada */
    .btn-invisible > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999; cursor: pointer;
    }
    
    /* Botones internos reales */
    .stButton > button {
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIÓN DE CARGA (Protegida)
@st.cache_data(show_spinner=False)
def cargar_datos_seguros():
    n, c, b = ["Mi Señora"], ["¿Qué le dice un pan a otro pan? Te presento una miga."], "Eres el papá de Ignacita."
    try:
        url_base = st.secrets["connections"]["gsheets"]["spreadsheet"].split('/edit')[0] + "/"
        n = pd.read_csv(f"{url_base}export?format=csv&sheet=Senoras").iloc[:, 0].dropna().tolist()
        c = pd.read_csv(f"{url_base}export?format=csv&sheet=Chistes").iloc[:, 0].dropna().tolist()
        b = " ".join(pd.read_csv(f"{url_base}export?format=csv&sheet=Contexto").iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass
    return n, c, b

# 4. LÓGICA DE ESTADOS
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    # --- PORTADA ---
    st.markdown(f'''
        <div class="portada-negra">
            <img src="

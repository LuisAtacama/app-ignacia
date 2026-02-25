import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA (ESTO VA PRIMERO)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. MOTOR DE CARGA BLINDADO (MEMORIA INTERNA)
@st.cache_data(show_spinner=False)
def obtener_datos_drive(url_spreadsheet):
    # Valores por defecto por si falla la conexión
    s = ["Señora"]
    ch = ["¿Qué le dice un pan a otro pan? Te presento a una miga."]
    adn = "Eres Luis, el papá de Ignacita. Habla de USTED."
    
    try:
        base = url_spreadsheet.split('/edit')[0]
        if not base.endswith("/"): base += "/"
        
        # Leemos los archivos de forma puramente técnica (sin st.write)
        df_s = pd.read_csv(f"{base}export?format=csv&sheet=Senoras")
        if not df_s.empty: s = df_s.iloc[:, 0].dropna().astype(str).tolist()
        
        df_ch = pd.read_csv(f"{base}export?format=csv&sheet=Chistes")
        if not df_ch.empty: ch = df_ch.iloc[:, 0].dropna().astype(str).tolist()
        
        df_adn = pd.read_csv(f"{base}export?format=csv&sheet=Contexto")
        if not df_adn.empty: adn = " ".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass
    return s, ch, adn

# Cargamos los datos en variables invisibles
SPREADSHEET_URL = st.secrets["connections"]["gsheets"]["spreadsheet"]
LISTA_SENORAS, LISTA_CHISTES, ADN_SISTEMA = obtener_datos_drive(SPREADSHEET_URL)

# 3. ESTILOS CSS (PORTADA Y BOTONES)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999; cursor: pointer;
    }
    .boton-interno button {
        position: relative !important; width: 100% !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
        z-index: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE NAVEGACIÓN
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    # --- PANTALLA NEGRA ---
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR"):
        st.session_state.autenticado = True
        st.session_state.mi_senora = random.choice(LISTA_SENORAS)
        st.rerun()
else:
    # --- INTERIOR LIMPIO ---
    st.title(f"❤️ ¡Hola, mi {st.session_state.mi_senora}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style

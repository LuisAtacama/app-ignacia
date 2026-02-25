import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS para que la portada sea negra, el logo esté centrado y el botón cubra TODO
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-contenedor {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    .stButton button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 1001; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Conexión a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# ==========================================
# 2. MOTOR DE CARGA (A PRUEBA DE ERRORES)
# ==========================================
def cargar_datos_maestros():
    # Valores de respaldo por si el Drive falla
    senoras = ["Loquita", "Molita", "Pepinita"]
    chistes = ["— ¿Qué le dice un pan a otro pan? — Te presento una miga."]
    adn_pasado = "Eres Luis, el papá de Ignacita. Habla de USTED."
    
    if conn:
        try:
            # Leemos las pestañas directamente
            df_s = conn.read(worksheet="Senoras", ttl=0)
            if df_s is not None and not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()
            
            df_adn = conn.read(worksheet="Contexto", ttl=0)
            if df_adn is not None and not df_adn.empty:
                adn_pasado = "\\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
        except Exception as e:
            # Si hay error 400, no bloqueamos la entrada
            pass
            
    return senoras, chistes, adn_pasado

if "DATOS_CARGADOS" not in st.session_state:
    s, ch, adn = cargar_datos_maestros()
    st.session_state.SENORAS = s
    st.session_state.CHISTES = ch
    st.session_state.ADN_MAESTRO = adn
    st.session_state.DATOS_CARGADOS = True

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN Y PORTADA
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    # CAPA VISUAL DE LA PORTADA
    st.markdown('''
        <div class="portada-contenedor">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    # EL BOTÓN INVISIBLE QUE CUBRE TODA LA PANTALLA
    if st.button("ENTRAR"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(st.session_state.SENORAS)
        st.rerun()
else:
    # PANTALLA PRINCIPAL (Lo que ve Ignacita al entrar)
    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.senora_actual}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    st.write("### 💬 Chat con pAAPi")
    st.info("¡Ya estamos dentro, mi amor! ¿En qué le puedo ayudar hoy?")
    # Aquí puede seguir agregando la lógica del chat...

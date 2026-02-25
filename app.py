import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# Inyectar CSS para la portada negra y diseño
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stAppViewContainer"] { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 60%; max-width: 400px; z-index: 1000; }
    .boton-invisible {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        opacity: 0; z-index: 1001; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Conexión a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# ==========================================
# 2. MOTOR DE CARGA (EVITAR ERROR 400)
# ==========================================
def cargar_datos_maestros():
    senoras = ["Loquita", "Molita", "Pepinita"]
    chistes = ["— ¿Qué le dice un pan a otro pan? — Te presento una miga."]
    adn_pasado = "Eres Luis, el papá de Ignacita. Habla de USTED."
    aprendizajes_recientes = ""

    if conn:
        try:
            # Intentamos leer con un método alternativo si el directo falla
            url_sheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
            
            # Pestaña Senoras
            df_s = conn.read(spreadsheet=url_sheet, worksheet="Senoras")
            if df_s is not None and not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()
            
            # Pestaña Contexto
            df_adn = conn.read(spreadsheet=url_sheet, worksheet="Contexto")
            if df_adn is not None and not df_adn.empty:
                adn_pasado = "\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
        except Exception as e:
            st.warning(f"Conectando en modo seguro... ({e})")
            
    return senoras, chistes, adn_pasado, aprendizajes_recientes

if "DATOS_CARGADOS" not in st.session_state:
    s, ch, adn, ap = cargar_datos_maestros()
    st.session_state.SENORAS = s
    st.session_state.CHISTES = ch
    st.session_state.ADN_MAESTRO = adn
    st.session_state.DATOS_CARGADOS = True

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    # MOSTRAR PORTADA NEGRA
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="width:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="btn_entrar", help="Haz clic para entrar"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(st.session_state.SENORAS)
        st.rerun()
else:
    # PANTALLA PRINCIPAL
    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.get('senora_actual', 'Señora')}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg")
    
    st.write("### 💬 Chat con pAAPi")
    # Aquí iría el resto de la lógica del chat

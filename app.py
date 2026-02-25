import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

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
    .boton-interno button {
        position: relative !important; width: auto !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# ==========================================
# 2. MOTOR DE CARGA (SIN NOMBRES DE RESPALDO)
# ==========================================
def cargar_datos_maestros():
    # Ahora empezamos vacíos para SABER si conectó
    senoras = []
    chistes = []
    adn_pasado = ""
    error_conexion = None
    
    if conn:
        try:
            # Leemos las pestañas
            df_s = conn.read(worksheet="Senoras", ttl=0)
            if df_s is not None and not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()
            
            df_ch = conn.read(worksheet="Chistes", ttl=0)
            if df_ch is not None and not df_ch.empty:
                chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()

            df_adn = conn.read(worksheet="Contexto", ttl=0)
            if df_adn is not None and not df_adn.empty:
                adn_pasado = "\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
        except Exception as e:
            error_conexion = str(e)
            
    # Si después de intentar sigue vacío, usamos un aviso real
    if not senoras:
        senoras = ["Señora (Sin Conexión)"]
        chistes = ["El Drive no respondió."]
        adn_pasado = "Eres un asistente básico porque el Drive falló."
        
    return senoras, chistes, adn_pasado, error_conexion

# Cargar datos
SENORAS, CHISTES, ADN_MAESTRO, ERROR_DRIVE = cargar_datos_maestros()

FOTOS = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg"]

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(f'''
        <div class="portada-contenedor">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="main_enter"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(SENORAS)
        st.session_state.foto_actual = random.choice(FOTOS)
        st.rerun()

else:
    # Si hubo error de Drive, lo mostramos arriba para saber
    if ERROR_DRIVE:
        st.error(f"⚠️ Error de conexión al Drive: {ERROR_DRIVE}")

    st.title(f"❤️ ¡Hola, mi {st.session_state.senora_actual}!")
    st.image(st.session_state.foto_actual, use_container_width=True)
    
    st.markdown('<div class="boton-interno">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="btn_chiste"):
        st.info(random.choice(CHISTES))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Qué me quiere decir, mi amor?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_MAESTRO}] + st.session_state.messages
            )
            full_response = response.choices[0].message.content
        except:
            full_response = "Error en OpenAI."

        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

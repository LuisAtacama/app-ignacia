import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS para portada y corregir visibilidad de botones
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
        display: inline-flex !important;
    }
    </style>
""", unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

def cargar_datos_maestros():
    # Inicializamos vacíos para validar la conexión real
    senoras, chistes, adn_pasado, error_log = [], [], "", None
    
    if conn:
        try:
            # Intentamos leer la pestaña Senoras del archivo definido en Secrets
            df_s = conn.read(worksheet="Senoras", ttl=0)
            if df_s is not None and not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()
            
            df_ch = conn.read(worksheet="Chistes", ttl=0)
            if df_ch is not None and not df_ch.empty:
                chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()

            df_adn = conn.read(worksheet="Contexto", ttl=0)
            if df_adn is not None and not df_adn.empty:
                adn_pasado = "\\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
        except Exception as e:
            error_log = str(e)
            
    # Si no hay datos del Drive, activamos el aviso de error
    if not senoras:
        senoras = ["Señora (Sin Conexión)"]
        chistes = ["Error: No se pudo conectar con el Drive."]
        adn_pasado = "Asistente básico por falla de conexión."
        
    return senoras, chistes, adn_pasado, error_log

# Carga de datos
SENORAS_DRIVE, CHISTES_DRIVE, ADN_DRIVE, ERROR_TECNICO = cargar_datos_maestros()
FOTOS = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg"]

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(f'''<div class="portada-contenedor"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre"></div>''', unsafe_allow_html=True)
    if st.button("ENTRAR"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(SENORAS_DRIVE)
        st.session_state.foto_actual = random.choice(FOTOS)
        st.rerun()
else:
    if ERROR_TECNICO:
        st.error(f"⚠️ Error de conexión al Drive: {ERROR_TECNICO}")

    st.title(f"❤️ ¡Hola, mi {st.session_state.senora_actual}!")
    st.image(st.session_state.foto_actual, use_container_width=True)
    
    # Botón WhatsApp Real
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)

    # Botón Chistes
    st.markdown('<div class="boton-interno">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!"):
        st.info(random.choice(CHISTES_DRIVE))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("¿Qué me quiere decir, mi amor?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": ADN_DRIVE}] + st.session_state.messages)
            full_res = res.choices[0].message.content
        except: full_res = "Error de conexión con la IA."
        with st.chat_message("assistant"): st.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})

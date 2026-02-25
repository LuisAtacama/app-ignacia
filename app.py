import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS para portada negra y diseño limpio
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
    /* Estilos para el chat y botones internos */
    .stChatInputContainer { bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Conexión a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# ==========================================
# 2. MOTOR DE CARGA (YA FUNCIONANDO)
# ==========================================
def cargar_datos_maestros():
    senoras = ["Loquita", "Molita", "Pepinita"]
    chistes = ["— ¿Qué le dice un pan a otro pan? — Te presento una miga."]
    adn_pasado = "Eres Luis, el papá de Ignacita. Habla de USTED."
    
    if conn:
        try:
            df_s = conn.read(worksheet="Senoras", ttl=0)
            if df_s is not None and not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()
            
            df_ch = conn.read(worksheet="Chistes", ttl=0)
            if df_ch is not None and not df_ch.empty:
                chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()

            df_adn = conn.read(worksheet="Contexto", ttl=0)
            if df_adn is not None and not df_adn.empty:
                adn_pasado = "\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
        except Exception:
            pass
            
    return senoras, chistes, adn_pasado

if "DATOS_CARGADOS" not in st.session_state:
    s, ch, adn = cargar_datos_maestros()
    st.session_state.SENORAS = s
    st.session_state.CHISTES = ch
    st.session_state.ADN_MAESTRO = adn
    st.session_state.DATOS_CARGADOS = True

# Fotos para mostrar al azar
FOTOS = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg"]

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('''
        <div class="portada-contenedor">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(st.session_state.SENORAS)
        st.session_state.foto_actual = random.choice(FOTOS)
        st.rerun()

# ==========================================
# 4. PANTALLA PRINCIPAL (CHAT Y CHISTES)
# ==========================================
else:
    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.senora_actual}!")
    st.image(st.session_state.foto_actual, use_container_width=True)
    
    # Botón de WhatsApp
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)

    # Botón de Chistes
    if st.button("🤡 ¡Cuéntame un chiste!"):
        st.info(random.choice(st.session_state.CHISTES))

    st.divider()
    st.write("### 💬 Chat con pAAPi")

    # Historial de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada del Chat
    if prompt := st.chat_input("¿Qué me quiere decir, mi amor?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Respuesta de la IA con el ADN del Drive
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": st.session_state.ADN_MAESTRO}] + st.session_state.messages
            )
            full_response = response.choices[0].message.content
        except:
            full_response = "Pucha mi amor, se me cortó la señal, pero pAAPi te adora."

        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

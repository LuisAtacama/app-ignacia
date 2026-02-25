import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. MOTOR DE CARGA (SILENCIOSO Y SEGURO)
@st.cache_data(show_spinner=False)
def cargar_adn_secreto(url_sheet):
    # Valores de respaldo por si el Drive falla
    nombres, bromas, bio = ["Señora"], ["¿Qué le dice un pan a otro pan? Te presento a una miga."], "Eres Luis, el papá de Ignacita."
    try:
        limpio = url_sheet.split('/edit')[0]
        if not limpio.endswith("/"): limpio += "/"
        
        # Cargamos datos de forma técnica, sin st.write ni impresiones en pantalla
        df_s = pd.read_csv(f"{limpio}export?format=csv&sheet=Senoras")
        if not df_s.empty: nombres = df_s.iloc[:, 0].dropna().astype(str).tolist()
        
        df_ch = pd.read_csv(f"{limpio}export?format=csv&sheet=Chistes")
        if not df_ch.empty: bromas = df_ch.iloc[:, 0].dropna().astype(str).tolist()
        
        df_adn = pd.read_csv(f"{limpio}export?format=csv&sheet=Contexto")
        if not df_adn.empty: bio = " ".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass
    return nombres, bromas, bio

# Cargamos el material del Drive a la memoria interna
URL_DRIVE = st.secrets["connections"]["gsheets"]["spreadsheet"]
APODOS, CHISTES_LISTA, ADN_CHAT = cargar_adn_secreto(URL_DRIVE)

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
    # MOSTRAR PORTADA NEGRA
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="gatillo"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(APODOS)
        st.rerun()
else:
    # INTERIOR DE LA APP LIMPIO
    st.title(f"❤️ ¡Hola, mi {st.session_state.senora_actual}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # Botón WhatsApp (Corregido para evitar SyntaxError)
    link_wa = "https://wa.me/56992238085"
    st.markdown(f'<a href="{link_wa}" target="_blank" style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)

    st.markdown('<div class="boton-interno">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="chiste_btn"):
        st.info(random.choice(CHISTES_LISTA))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("¿Qué me quiere decir, mi amor?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_CHAT}] + st.session_state.messages
            )
            r = res.choices[0].message.content
        except:
            r = "Pucha mi amor, se me cortó la señal, pero pAAPi te adora."

        with st.chat_message("assistant"):
            st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})

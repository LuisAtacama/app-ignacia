import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN (Debe ser lo primero)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. CARGA DE DATOS (Silenciosa)
@st.cache_data(show_spinner=False)
def cargar_todo():
    n, c, b = ["Mi Señora"], ["¿Chiste? No cargó el Drive."], "Eres el papá de Ignacita."
    try:
        url = st.secrets["connections"]["gsheets"]["spreadsheet"].split('/edit')[0] + "/"
        n = pd.read_csv(url + "export?format=csv&sheet=Senoras").iloc[:, 0].dropna().tolist()
        c = pd.read_csv(url + "export?format=csv&sheet=Chistes").iloc[:, 0].dropna().tolist()
        b = " ".join(pd.read_csv(url + "export?format=csv&sheet=Contexto").iloc[:, 0].dropna().astype(str).tolist())
    except: pass
    return n, c, b

# 3. ESTILOS CSS (Botón invisible que manda sobre todo)
st.markdown("""
<style>
    .stApp { background-color: white; }
    .portada {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 10;
    }
    .logo { position: absolute; width: 80%; max-width: 500px; z-index: 20; pointer-events: none; }
    
    /* ESTE BOTÓN OCUPA TODA LA PANTALLA Y ESTÁ AL FRENTE */
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important;
        color: transparent !important; z-index: 9999 !important;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 4. LÓGICA
if "entrado" not in st.session_state:
    st.session_state.entrado = False

if not st.session_state.entrado:
    # Muestra la portada
    st.markdown('<div class="portada"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo"></div>', unsafe_allow_html=True)
    # Botón único
    if st.button("ENTRAR", key="main_gate"):
        st.session_state.entrado = True
        st.rerun()
else:
    # INTERIOR
    APODOS, CHISTES, ADN_SISTEMA = cargar_todo()
    if "saludo" not in st.session_state:
        st.session_state.saludo = random.choice(APODOS)

    st.title(f"❤️ ¡Hola, mi {st.session_state.saludo}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # WhatsApp y Chistes
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:10px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, chiste!", key="j"): st.info(random.choice(CHISTES))

    st.divider()
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Dime algo..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":ADN_SISTEMA}]+st.session_state.chat)
            r = res.choices[0].message.content
        except: r = "Se cortó la señal..."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

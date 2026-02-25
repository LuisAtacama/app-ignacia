import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. CARGA DE DATOS (Arreglada para que NO falle)
@st.cache_data(show_spinner=False)
def cargar_todo():
    # Valores por si falla el Drive
    n = ["Mi Señora", "Loquita", "Molita"]
    c = ["¿Qué le dice un pan a otro pan? Te presento a una miga."]
    b = "Eres Luis, el papá de Ignacita. Habla de USTED."
    try:
        url_base = st.secrets["connections"]["gsheets"]["spreadsheet"].split('/edit')[0] + "/"
        # Pestaña Señoras
        df_n = pd.read_csv(f"{url_base}export?format=csv&sheet=Senoras")
        if not df_n.empty: n = df_n.iloc[:, 0].dropna().astype(str).tolist()
        # Pestaña Chistes
        df_c = pd.read_csv(f"{url_base}export?format=csv&sheet=Chistes")
        if not df_c.empty: c = df_c.iloc[:, 0].dropna().astype(str).tolist()
        # Pestaña Contexto (ADN)
        df_b = pd.read_csv(f"{url_base}export?format=csv&sheet=Contexto")
        if not df_b.empty: b = " ".join(df_b.iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass
    return n, c, b

# 3. DISEÑO CSS (Portada e Interfaz)
st.markdown("""
<style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    .btn-invisible > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999 !important; cursor: pointer;
    }
    .stButton > button { width: 100%; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE NAVEGACIÓN
if "entrado" not in st.session_state:
    st.session_state.entrado = False

if not st.session_state.entrado:
    # --- PORTADA ---
    st.markdown('<div class="portada-negra"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre"></div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-invisible">', unsafe_allow_html=True)
    if st.button("ENTRAR", key="gate_key"):
        st.session_state.entrado = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- INTERIOR ---
    APODOS, CHISTES, ADN_SISTEMA = cargar_todo()
    
    if "saludo" not in st.session_state:
        st.session_state.saludo = random.choice(APODOS)

    st.title(f"❤️ ¡Hola, mi {st.session_state.saludo}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # Botón WhatsApp
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 15px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)

    # Botón Chistes (AHORA SÍ APARECE)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="joke"):
        st.info(random.choice(CHISTES))

    st.divider()
    
    # CHAT
    if "chat" not in st.session_state:
        st.session_state.chat = []
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_SISTEMA}] + st.session_state.chat
            )
            r = res.choices[0].message.content
        except:
            r = "Pucha mi amor, se me cortó la señal, pero pAAPi te adora."
        
        with st.chat_message("assistant"):
            st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

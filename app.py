import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN (Debe ser lo primero absoluto)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. MOTOR DE CARGA CON SALVAVIDAS
@st.cache_data(ttl=600, show_spinner="Cargando el amor de pAAPi...")
def cargar_datos_seguros(url_spreadsheet):
    # Valores de respaldo por si el Drive no contesta rápido
    n = ["Señora", "Loquita", "Molita"]
    c = ["¿Qué le dice un pan a otro pan? Te presento a una miga."]
    b = "Eres Luis, el papá de Ignacita. Habla de USTED."
    try:
        base = url_spreadsheet.split('/edit')[0]
        if not base.endswith("/"): base += "/"
        # Lectura técnica directa a variables
        df_n = pd.read_csv(f"{base}export?format=csv&sheet=Senoras")
        if not df_n.empty: n = df_n.iloc[:, 0].dropna().astype(str).tolist()
        df_c = pd.read_csv(f"{base}export?format=csv&sheet=Chistes")
        if not df_c.empty: c = df_c.iloc[:, 0].dropna().astype(str).tolist()
        df_b = pd.read_csv(f"{base}export?format=csv&sheet=Contexto")
        if not df_b.empty: b = " ".join(df_b.iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass # Si falla, usa los valores de respaldo silenciosamente
    return n, c, b

# Carga de datos
URL_D = st.secrets["connections"]["gsheets"]["spreadsheet"]
APODOS, BROMAS, ADN_IA = cargar_datos_seguros(URL_D)

# 3. DISEÑO CSS (PORTADA Y BOTONES)
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
    .btn-interno button {
        position: relative !important; width: 100% !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
        z-index: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE NAVEGACIÓN
if "entrado" not in st.session_state:
    st.session_state.entrado = False

if not st.session_state.entrado:
    # --- PORTADA ---
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="gate"):
        st.session_state.entrado = True
        st.session_state.saludo_act = random.choice(APODOS)
        st.rerun()
else:
    # --- INTERIOR LIMPIO ---
    st.title(f"❤️ ¡Hola, mi {st.session_state.saludo_act}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # WhatsApp (Formato ultra-seguro)
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)

    # Chistes
    st.markdown('<div class="btn-interno">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="joke"):
        st.info(random.choice(BROMAS))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    if "historial" not in st.session_state: st.session_state.historial = []
    for m in st.session_state.historial:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.historial.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_IA}] + st.session_state.historial
            )
            r = res.choices[0].message.content
        except: r = "Pucha mi amor, se me cortó la señal, pero pAAPi te adora."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.historial.append({"role": "assistant", "content": r})

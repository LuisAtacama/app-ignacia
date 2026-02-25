import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN INICIAL (Debe ser lo primero)
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. MOTOR DE CARGA ULTRA-SILENCIOSO (Capa de Invisibilidad)
@st.cache_data(show_spinner=False)
def cargar_todo_el_drive(url_spreadsheet):
    # Valores de respaldo por si falla la conexión
    n, c, b = ["Señora"], ["¿Qué le dice un pan a otro pan? Te presento una miga."], "Eres Luis, el papá de Ignacita."
    try:
        # Preparamos el link base para exportación directa de CSV
        base = url_spreadsheet.split('/edit')[0]
        if not base.endswith("/"): base += "/"
        
        # Lectura técnica de datos (Sin st.write, sin impresiones)
        # Cargamos nombres de la pestaña 'Senoras'
        df_n = pd.read_csv(f"{base}export?format=csv&sheet=Senoras")
        if not df_n.empty: n = df_n.iloc[:, 0].dropna().astype(str).tolist()
        
        # Cargamos chistes de la pestaña 'Chistes'
        df_c = pd.read_csv(f"{base}export?format=csv&sheet=Chistes")
        if not df_c.empty: c = df_c.iloc[:, 0].dropna().astype(str).tolist()
        
        # Cargamos el ADN de la pestaña 'Contexto' (Solo lo guardamos en la variable 'b')
        df_b = pd.read_csv(f"{base}export?format=csv&sheet=Contexto")
        if not df_b.empty: b = " ".join(df_b.iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass
    return n, c, b

# Ejecutamos la carga secreta
URL_DE_SECRETS = st.secrets["connections"]["gsheets"]["spreadsheet"]
APODOS, LISTA_CHISTES, ADN_SISTEMA = cargar_todo_el_drive(URL_DE_SECRETS)

# 3. DISEÑO CSS (PORTADA Y BOTONES)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    
    /* El botón invisible para entrar desde la portada */
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999; cursor: pointer;
    }
    
    /* Estilo para los botones internos (Chistes) */
    .boton-chiste button {
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
    # --- PANTALLA DE PORTADA ---
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR"):
        st.session_state.autenticado = True
        # Elegimos un apodo real del Drive para el saludo
        st.session_state.mi_senora = random.choice(APODOS)
        st.rerun()
else:
    # --- INTERIOR DE LA APP LIMPIO ---
    st.title(f"❤️ ¡Hola, mi {st.session_state.mi_senora}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # WhatsApp
    st.markdown(f'<a href="https://wa.me/56992238085" target="_blank" style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)

    # Botón de Chistes
    st.markdown('<div class="boton-chiste">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="chiste"):
        st.info(random.choice(LISTA_CHISTES))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # Historial de Chat
    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Cuadro de Chat
    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_SISTEMA}] + st.session_state.msgs
            )
            r = res.choices[0].message.content
        except:
            r = "Pucha mi amor, se me cortó la señal, pero pAAPi te adora."

        with st.chat_message("assistant"):
            st.markdown(r)
        st.session_state.msgs.append({"role": "assistant", "content": r})

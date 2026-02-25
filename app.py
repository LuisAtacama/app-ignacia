import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS para portada y limpieza visual
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    
    /* El botón invisible para entrar */
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999; cursor: pointer;
    }
    
    /* Botones internos una vez dentro */
    .boton-interno button {
        position: relative !important; width: 100% !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
        z-index: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. MOTOR DE CARGA (100% SILENCIOSO)
def cargar_datos_viva_voz():
    senoras, chistes, adn = ["Señora"], ["¿Qué le dice un pan a otro pan? Te presento a una miga."], "Eres Luis, el papá de Ignacita."
    try:
        # Obtenemos el link de Secrets y lo preparamos
        url_base = st.secrets["connections"]["gsheets"]["spreadsheet"].split('/edit')[0]
        if not url_base.endswith("/"): url_base += "/"
        
        # Leemos los datos de forma técnica, sin st.write ni impresiones
        df_s = pd.read_csv(f"{url_base}export?format=csv&sheet=Senoras")
        if not df_s.empty:
            senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()

        df_ch = pd.read_csv(f"{url_base}export?format=csv&sheet=Chistes")
        if not df_ch.empty:
            chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()

        df_adn = pd.read_csv(f"{url_base}export?format=csv&sheet=Contexto")
        if not df_adn.empty:
            # Aquí está el truco: guardamos el texto en una variable, NO en la pantalla
            adn = "\\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
    except:
        pass
    return senoras, chistes, adn

# Inicializar sesión si no existe
if "DATOS" not in st.session_state:
    s, ch, adn = cargar_datos_viva_voz()
    st.session_state.DATOS = {"s": s, "ch": ch, "adn": adn}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# 3. NAVEGACIÓN
if not st.session_state.autenticado:
    # --- PORTADA ---
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="trigger_entrar"):
        st.session_state.autenticado = True
        # Elegimos el apodo real del Drive
        st.session_state.mi_senora = random.choice(st.session_state.DATOS["s"])
        st.rerun()
else:
    # --- INTERIOR ---
    st.title(f"❤️ ¡Hola, mi {st.session_state.mi_senora}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # Botón WhatsApp
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)

    # Botón Chistes
    st.markdown('<div class="boton-interno">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="btn_chiste"):
        st.info(random.choice(st.session_state.DATOS["ch"]))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # Lógica del Chat
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
                messages=[{"role": "system", "content": st.session_state.DATOS["adn"]}] + st.session_state.messages
            )
            r = res.choices[0].message.content
        except:
            r = "Pucha mi amor, se me cortó la señal, pero pAAPi te adora."

        with st.chat_message("assistant"):
            st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})

import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN E INICIALIZACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS para portada y botones
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-contenedor {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    .btn-portada button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 1001; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 2. MOTOR DE CARGA MANUAL (EVITA EL ERROR 400)
def cargar_datos_viva_voz():
    senoras, chistes, adn, error = [], [], "", None
    try:
        # Usamos la URL base de los secrets
        base_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        # Limpiamos la URL por si acaso
        base_url = base_url.replace("/edit", "").replace("?usp=sharing", "")
        if not base_url.endswith("/"): base_url += "/"
        
        # Leemos las pestañas como CSV (esto se salta el Error 400 de la librería)
        url_senoras = f"{base_url}gviz/tq?tqx=out:csv&sheet=Senoras"
        url_chistes = f"{base_url}gviz/tq?tqx=out:csv&sheet=Chistes"
        url_contexto = f"{base_url}gviz/tq?tqx=out:csv&sheet=Contexto"

        df_s = pd.read_csv(url_senoras)
        senoras = df_s.iloc[:, 0].dropna().tolist()

        df_ch = pd.read_csv(url_chistes)
        chistes = df_ch.iloc[:, 0].dropna().tolist()

        df_adn = pd.read_csv(url_contexto)
        adn = "\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())

    except Exception as e:
        error = str(e)
    
    if not senoras:
        senoras = ["Señora (Sin Conexión)"]
        chistes = ["No se pudieron cargar los chistes."]
        adn = "Eres un asistente básico."
    
    return senoras, chistes, adn, error

# Cargar datos
if "DATOS" not in st.session_state:
    s, ch, adn, err = cargar_datos_viva_voz()
    st.session_state.DATOS = {"s": s, "ch": ch, "adn": adn, "err": err}

FOTOS = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg"]

# 3. NAVEGACIÓN
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(f'<div class="portada-contenedor"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre"></div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-portada">', unsafe_allow_html=True)
    if st.button("ENTRAR", key="portada_btn"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(st.session_state.DATOS["s"])
        st.session_state.foto_actual = random.choice(FOTOS)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Si sigue el error, lo mostramos para diagnosticar
    if st.session_state.DATOS["err"] and "400" in st.session_state.DATOS["err"]:
        st.warning("⚠️ Google Sheets pide permisos. Asegúrese de que el archivo esté como 'Cualquier persona con el enlace' en modo 'Editor'.")

    st.title(f"❤️ ¡Hola, mi {st.session_state.senora_actual}!")
    st.image(st.session_state.foto_actual, use_container_width=True)
    
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)

    if st.button("🤡 ¡Papi, cuéntame un chiste!"):
        st.info(random.choice(st.session_state.DATOS["ch"]))

    st.divider()
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("¿Qué me quiere decir, mi amor?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": st.session_state.DATOS["adn"]}] + st.session_state.messages)
            r = res.choices[0].message.content
        except: r = "Pucha mi amor, OpenAI no respondió."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content":

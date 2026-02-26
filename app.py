import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="pAAPi", page_icon="🎀", layout="centered")

# 2. FUNCIÓN DE LECTURA LIMPIA (El Escudo)
def leer_archivo_limpio(nombre, es_adn=False):
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
                for r in ['Ñ', 'ï»¿', 'Â', '\ufffd']:
                    texto = texto.replace(r, '')
                if es_adn: return texto.strip()
                return [line.strip() for line in texto.split('\n') if line.strip()]
    except: pass
    return "Eres Luis, el papá de Ignacita." if es_adn else []

# CARGA DE DATOS
ADN_SISTEMA = leer_archivo_limpio("adn.txt", es_adn=True)
APODOS = leer_archivo_limpio("senoras.txt")
LISTA_CHISTES = leer_archivo_limpio("chistes.txt")
LISTA_FOTOS = leer_archivo_limpio("fotos.txt")
LISTA_VIDEOS = leer_archivo_limpio("videos.txt")

# 3. LÓGICA DE NAVEGACIÓN
if "entrado" not in st.session_state:
    st.session_state.entrado = False

# --- PANTALLA DE PORTADA (LOGO ARRIBA, VIDEO ABAJO) ---
if not st.session_state.entrado:
    st.markdown("""
    <style>
        .stApp { background-color: black; }
        .portada-full {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: black; z-index: 1000; overflow: hidden;
        }
        .logo-superior {
            width: 80%; max-width: 450px;
            margin-bottom: 30px; z-index: 1001;
        }
        .video-gif {
            height: 55vh; width: auto;
            object-fit: contain; z-index: 1000;
        }
        .stButton > button {
            position: fixed !important; top: 0 !important; left: 0 !important;
            width: 100vw !important; height: 100vh !important;
            background: transparent !important; border: none !important;
            color: transparent !important; z-index: 99999 !important;
            cursor: pointer !important;
        }
    </style>
    <div class="portada-full">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-superior">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-gif">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="boton_invisible"):
        st.session_state.entrado = True
        # Cambio solicitado: Sin el "mi"
        adj = random.choice(APODOS) if APODOS else "Dinosauria"
        st.session_state.saludo_nombre = f"señora {adj}"
        st.rerun()

# --- INTERIOR ---
else:
    st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)
    
    # 1. Saludo Dinámico Ajustado
    st.title(f"❤️ ¡Hola, {st.session_state.saludo_nombre}!")
    
    # 2. Multimedia Aleatoria
    todo_multimedia = [(f, "foto") for f in LISTA_FOTOS] + [(v, "video") for v in LISTA_VIDEOS]
    if todo_multimedia:
        item, tipo = random.choice(todo_multimedia)
        if tipo == "foto":
            st.image(item, use_container_width=True)
        else:
            st.video(item)

    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:15px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    if st.button("🤡 ¡Papi, cuéntame un chiste!", use_container_width=True):
        if LISTA_CHISTES:
            st.info(random.choice(LISTA_CHISTES))

    st.divider()

    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Dime algo, mi amor..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            instrucciones = f"{ADN_SISTEMA}\n\nREGLA: Eres Luis, el papá de Ignacita. Ella es tu 'señora' (apodo). Habla con amor de padre."
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": instrucciones}] + st.session_state.chat
            )
            respuesta = res.choices[0].message.content
        except:
            respuesta = "Pucha mi vida, se me cortó el internet, pero aquí estoy para ti."

        with st.chat_message("assistant"): st.markdown(respuesta)
        st.session_state.chat.append({"role": "assistant", "content": respuesta})

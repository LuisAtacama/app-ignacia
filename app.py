import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi", page_icon="🎀", layout="centered")

# 2. FUNCIÓN ESCUDO
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

if "entrado" not in st.session_state:
    st.session_state.entrado = False

# --- PORTADA PROFESIONAL (LOGO EMERGIENDO) ---
if not st.session_state.entrado:
    st.markdown("""
    <style>
        .stApp { background-color: black; }
        .portada-contenedor {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: black; z-index: 1000; overflow: hidden;
        }
        /* EL LOGO QUE EMERGE SUAVEMENTE */
        .logo-pappi {
            position: absolute;
            top: 15%; 
            width: 75%; max-width: 480px;
            z-index: 1002;
            animation: aparecer 2.5s ease-out;
        }
        @keyframes aparecer {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        /* EL GIF DE FONDO */
        .video-gif {
            width: 100%; height: 100%;
            object-fit: cover; /* Para que llene la pantalla como en su captura */
            z-index: 1001;
        }
        /* CAPA INVISIBLE PARA CLICK TOTAL */
        .stButton > button {
            position: fixed !important; top: 0 !important; left: 0 !important;
            width: 100vw !important; height: 100vh !important;
            background: transparent !important; border: none !important;
            color: transparent !important; z-index: 99999 !important;
        }
    </style>
    <div class="portada-contenedor">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-pappi">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-gif">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="entrar_total"):
        st.session_state.entrado = True
        adj = random.choice(APODOS) if APODOS else "Dinosauria"
        st.session_state.saludo_nombre = f"señora {adj}"
        st.rerun()

# --- INTERIOR DE LA APP ---
else:
    st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)
    st.title(f"❤️ ¡Hola, {st.session_state.saludo_nombre}!")
    
    # Multimedia Aleatoria
    todo_m = [(f, "foto") for f in LISTA_FOTOS] + [(v, "video") for v in LISTA_VIDEOS]
    if todo_m:
        item, tipo = random.choice(todo_m)
        if tipo == "foto": st.image(item, use_container_width=True)
        else: st.video(item)

    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:15px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    if st.button("🤡 ¡Papi, cuéntame un chiste!", use_container_width=True):
        if LISTA_CHISTES: st.info(random.choice(LISTA_CHISTES))

    st.divider()
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # SALUDO PERSONALIZADO EN EL CUADRO
    if p := st.chat_input("Cuénteme algo mi niñita"):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            instr = f"{ADN_SISTEMA}\nREGLA: Eres el papá Luis hablando con su hija Ignacita."
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": instr}] + st.session_state.chat)
            r = res.choices[0].message.content
        except: r = "Se cortó la señal, mi niña, pero aquí estoy."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

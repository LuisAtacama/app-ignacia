import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. FUNCIÓN DE LECTURA LIMPIA
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
    return "Eres Luis, el papá de Ignacita." if es_adn else ["Dinosauria"]

ADN_SISTEMA_BASE = leer_archivo_limpio("adn.txt", es_adn=True)
APODOS = leer_archivo_limpio("senoras.txt")
LISTA_CHISTES = leer_archivo_limpio("chistes.txt")

# REFUERZO DE PERSONALIDAD: Obligamos a la IA a recordar que habla con SU HIJA
ADN_REFORZADO = f"""
{ADN_SISTEMA_BASE}

INSTRUCCIÓN CRUCIAL: Estás hablando DIRECTAMENTE con tu hija Ignacita (o sus apodos de señora). 
NUNCA respondas como si hablaras con Luis. Luis eres TÚ (el narrador). 
Usa frases como "mi amor", "hijita", "mi vida". 
Si ella pregunta por alguien, responde: "Es tu tío...", "Es tu abuela...", "Es amigo de tu papá (yo)".
"""

# 3. LÓGICA DE NAVEGACIÓN (Persistencia mejorada)
if "entrado" not in st.session_state:
    st.session_state.entrado = False

# --- PANTALLA DE PORTADA (LOGO ARRIBA Y CLICK TOTAL) ---
if not st.session_state.entrado:
    st.markdown("""
    <style>
        .stApp { background-color: black; }
        .portada-full {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: black;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            z-index: 1000;
        }
        .logo-superior {
            margin-top: 50px;
            width: 70%;
            max-width: 400px;
            z-index: 1001;
        }
        .video-fondo {
            width: 100%;
            max-height: 60vh;
            object-fit: contain;
            margin-top: 20px;
            z-index: 1000;
        }
        .stButton > button {
            position: fixed !important;
            top: 0 !important; left: 0 !important;
            width: 100vw !important; height: 100vh !important;
            background: transparent !important;
            border: none !important;
            color: transparent !important;
            z-index: 99999 !important;
        }
    </style>
    <div class="portada-full">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-superior">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-fondo">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="click_total"):
        st.session_state.entrado = True
        adjetivo = random.choice(APODOS)
        st.session_state.nombre_saludo = f"señora {adjetivo}"
        st.rerun()

# --- INTERIOR DE LA APP ---
else:
    st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)
    
    # 1. Saludo: ¡Hola, mi señora [adjetivo]!
    st.title(f"❤️ ¡Hola, mi {st.session_state.nombre_saludo}!")
    
    # 2. Galería de Fotos Dinámica (Muestra una distinta cada vez que entra/actualiza)
    fotos = [
        "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg",
        "https://i.postimg.cc/Bb71JpGr/image.png" # Agregue aquí más links de sus fotos
    ]
    st.image(random.choice(fotos), use_container_width=True)
    
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:20px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    if st.button("🤡 ¡Papi, cuéntame un chiste!", use_container_width=True):
        st.info(random.choice(LISTA_CHISTES))

    st.divider()
    
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_REFORZADO}] + st.session_state.chat
            )
            r = res.choices[0].message.content
        except: r = "Pucha mi amor, se cortó la señal, pero pAAPi te adora."
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

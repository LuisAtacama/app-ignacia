import streamlit as st
import random
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y LISTADO DE CONTENIDO
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

ADJETIVOS = ["Inteligente", "Valiente", "Bella", "Artista", "Genia", "Poderosa", "Decidida", "Encantadora", "Brillante", "Única"]

# Galería de fotos
FOTOS_RANDOM = [
    "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg",
    "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg",
    "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg",
    "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg",
    "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg",
    "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg",
    "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg",
    "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg",
    "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg",
    "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg",
    "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg",
    "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg",
    "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg",
    "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg",
    "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg",
    "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg",
    "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg",
    "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg",
    "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg",
    "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg",
    "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg",
    "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg",
    "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg",
    "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg",
    "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"
]

# Lista de videos de YouTube
VIDEOS_RANDOM = [
    "https://youtu.be/sB-TdQKWMGI", "https://youtu.be/IBExxlSBbdE",
    "https://youtu.be/4Bt2LytMb-o", "https://youtu.be/SLhpt5vxQIw",
    "https://youtu.be/6Qz637nhLKc", "https://youtu.be/zBN-6NEGyzM",
    "https://youtu.be/leAF95qMGCg", "https://youtu.be/Rgl4n3jWGCQ"
]

# ==========================================
# 2. IA: ADN LUIS v6.4
# ==========================================
def generar_respuesta_papi(mensaje_usuario, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt_sistema = "Eres Luis, papá de Ignacia. Chileno, tierno. Habla siempre de USTED. Nunca tutees. Usa apodos como mi amorcito o hijita. Pregunta ¿Cómo está usted?"
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-4:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})
        response = client.chat.completions.create(model="gpt-4o-mini", messages=mensajes, temperature=0.6)
        return response.choices[0].message.content
    except:
        return "Pucha mi amorcito, algo pasó con la señal, pero aquí está su pAAPi. ¡Vivaldi!"

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN
# ==========================================
if "chat" in st.query_params:
    st.session_state.pagina = 'principal'
else:
    st.session_state.pagina = 'inicio'

# --- PANTALLA DE INICIO ---
if st.session_state.pagina == 'inicio':
    st.markdown("""<style>
        [data-testid="stAppViewContainer"] { background-color: black !important; }
        .portada-wrapper { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; display: flex; align-items: center; justify-content: center; z-index: 999; }
        .video-gif { max-width: 100%; max-height: 100%; object-fit: contain; }
        .logo-sobre { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 70%; max-width: 350px; animation: emerger 2.5s ease-out forwards; }
        @keyframes emerger { 0% { opacity: 0; transform: translate(-50%, -50%) scale(0.6); } 100% { opacity: 1; transform: translate(-50%, -50%) scale(1); } }
        .stButton button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; opacity: 0; z-index: 1000; cursor: pointer; }
    </style>""", unsafe_allow_html=True)

    if st.button("ENTRAR"):
        st.query_params["chat"] = "true"
        st.session_state.adjetivo = random.choice(ADJETIVOS)
        # Decidir si mostrar foto o video
        if random.random() > 0.5:
            st.session_state.contenido_actual = {"tipo": "foto", "url": random.choice(FOTOS_RANDOM)}
        else:
            st.session_state.contenido_actual = {"tipo": "video", "url": random.choice(VIDEOS_RANDOM)}
        st.rerun()

    st.markdown(f"""<div class="portada-wrapper">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-gif">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
    </div>""", unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL ---
else:
    st.markdown("""<style> [data-testid="stAppViewContainer"] { background-color: white !important; } </style>""", unsafe_allow_html=True)

    if 'adjetivo' not in st.session_state: st.session_state.adjetivo = random.choice(ADJETIVOS)
    if 'contenido_actual' not in st.session_state:
        st.session_state.contenido_actual = {"tipo": "foto", "url": random.choice(FOTOS_RANDOM)}

    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.adjetivo}!")
    st.subheader("¿Cómo está usted?")
    
    # Mostrar Foto o Video según lo elegido
    if st.session_state.contenido_actual["tipo"] == "foto":
        st.image(st.session_state.contenido_actual["url"], use_container_width=True)
    else:
        st.video(st.session_state.contenido_actual["url"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 14px; border-radius: 50px; text-decoration: none; font-weight: bold; width: 100%; max-width: 300px; text-align: center; display: block; margin: 0 auto;'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    
    st.divider()
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("Escriba aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        respuesta = generar_respuesta_papi(prompt, st.session_state.messages)
        with st.chat_message("assistant"): st.write(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

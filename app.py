import streamlit as st
import random
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# Inicializar estados para que no se pierdan al refrescar
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'
if 'saludo' not in st.session_state:
    st.session_state.saludo = ""

# ==========================================
# 2. IA: ADN LUIS v5.4 (Trato de Usted y Naturalidad)
# ==========================================
def generar_respuesta_papi_v4(mensaje_usuario, animo_actual, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        ahora = datetime.now().hour
        modo = "cierre_noche" if (ahora >= 21 or ahora <= 6) else "cariño"

        prompt_sistema = f"""
        Eres Luis, papá de Ignacia. Chileno, tierno y protector.
        REGLA DE ORO: Hable siempre de USTED. Nunca use 'tú'.
        APODOS: 'hijita', 'ignacita', 'mi chiquitita', 'mi amorcito'.
        REGLA CRÍTICA: No repita el mismo apodo en la misma respuesta. 
        Si usa 'Si mi amorcito dígame', no agregue más apodos.
        PROHIBIDO: 'amor' solo, 'mi vida', 'Ignacia' solo.
        PREGUNTA CLAVE: Use siempre '¿Cómo está usted?' o '¿Cómo va todo?'.
        ESTILO: Breve, cálido, chileno. MODO: {modo}.
        """
        
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-4:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            temperature=0.6
        )
        return response.choices[0].message.content
    except:
        return "Pucha mi amorcito, algo pasó con la señal, pero aquí está su pAAPi. ¡Vivaldi!"

# ==========================================
# 3. LÓGICA DE PANTALLAS
# ==========================================

# --- PANTALLA DE INICIO (PORTADA) ---
if st.session_state.pagina == 'inicio':
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { background-color: black !important; }
            .portada-wrapper {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: black; display: flex; align-items: center; justify-content: center;
                z-index: 999; overflow: hidden;
            }
            .video-gif { 
                max-width: 100%; max-height: 100%; 
                object-fit: contain; 
            }
            .logo-sobre {
                position: absolute; top: 50%; left: 50%;
                transform: translate(-50%, -50%); width: 70%; max-width: 350px;
                animation: emerger 2.5s ease-out forwards;
            }
            @keyframes emerger {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.6); }
                100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }
            .stButton > button {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                opacity: 0; z-index: 1000; cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("ENTRAR", key="boton_portada"):
        opciones = ["hijita", "ignacita", "mi chiquitita", "mi amorcito"]
        elegido = random.choice(opciones)
        # CORRECCIÓN: "Usted" en lugar de "se encuentra"
        st.session_state.saludo = f"❤️ ¡Hola, {elegido}! ¿Cómo está usted?"
        st.session_state.pagina = 'principal'
        st.rerun()

    st.markdown(f"""
        <div class="portada-wrapper">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-gif">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    """, unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL (CHAT) ---
else:
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { background-color: white !important; }
            .main { overflow-y: auto !important; }
        </style>
    """, unsafe_allow_html=True)

    # Mostrar saludo generado
    st.title(st.session_state.saludo)
    
    # CORRECCIÓN: "¿Cómo se siente usted?"
    animo = st.select_slider("¿Cómo se siente usted?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
    
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 14px; border-radius: 50px; text-decoration: none; font-weight: bold; width: 100%; max-width: 300px; text-align: center; display: block; margin: 0 auto;'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.info(random.choice(["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— ¿Qué le dice un pan a otro? — Te presento una miga."]))

    st.write("### 💬 Chat con pAAPi")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Escriba aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            respuesta = generar_respuesta_papi_v4(prompt, animo, st.session_state.messages)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

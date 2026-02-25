import streamlit as st
import random
import json
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN E INVENTARIO DE CONTENIDO
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

ADJETIVOS = ["Inteligente", "Valiente", "Bella", "Artista", "Genia", "Poderosa"]
APODOS = ["hijita", "ignacita", "mi chiquitita", "mi amorcito"]

# Diccionario de fotos según ánimo (Don Luis, cambie estos links después)
FOTOS_ANIMO = {
    "MUY TRISTE": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg",
    "TRISTE": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg",
    "NORMAL": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg",
    "FELIZ": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg",
    "MUY FELIZ": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg"
}

# ==========================================
# 2. GESTIÓN DE ESTADO (MEMORIA)
# ==========================================
# Si el usuario ya entró, mantenemos la sesión incluso al refrescar
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if 'adjetivo' not in st.session_state:
    st.session_state.adjetivo = random.choice(ADJETIVOS)

if 'apodo' not in st.session_state:
    st.session_state.apodo = random.choice(APODOS)

# ==========================================
# 3. LÓGICA DE PANTALLAS
# ==========================================

# --- PANTALLA DE INICIO (PORTADA) ---
if not st.session_state.autenticado:
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { background-color: black !important; }
            .portada-full {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: black; display: flex; align-items: center; justify-content: center;
                z-index: 999; overflow: hidden; cursor: pointer;
            }
            .video-fondo { max-width: 100%; max-height: 100%; object-fit: contain; }
            .logo-sobre {
                position: absolute; top: 50%; left: 50%;
                transform: translate(-50%, -50%); width: 70%; max-width: 400px;
                animation: emerger 2.5s ease-out forwards;
            }
            @keyframes emerger {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.6); }
                100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }
            .stButton button {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                opacity: 0; z-index: 1000;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("ENTRAR", key="entrar_btn"):
        st.session_state.autenticado = True
        st.rerun()

    st.markdown(f"""
        <div class="portada-full">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-fondo">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    """, unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL ---
else:
    st.markdown("""<style>
        [data-testid="stAppViewContainer"] { background-color: white !important; }
        .main { overflow-y: auto !important; }
        /* Forzar scroll al inicio */
        html { scroll-behavior: smooth; }
    </style>""", unsafe_allow_html=True)

    # Saludo Correcto: Mi Señora + Adjetivo
    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.adjetivo}!")
    st.subheader(f"¿Cómo está usted, {st.session_state.apodo}?")
    
    # Selector de ánimo que cambia la foto
    animo = st.select_slider("¿Cómo se siente usted hoy?", 
                             options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], 
                             value="NORMAL")
    
    # La foto cambia según el slider
    st.image(FOTOS_ANIMO[animo], use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 14px; border-radius: 50px; text-decoration: none; font-weight: bold; width: 100%; max-width: 300px; text-align: center; display: block; margin: 0 auto;'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    
    st.divider()
    
    # Lógica del Chat (ADN LUIS)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("Escriba aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        # Respuesta IA
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Eres Luis, papá de Ignacia. Chileno, tierno. Habla de USTED. Usa apodos como {st.session_state.apodo}. No repitas apodos. Pregunta ¿Cómo está usted?"},
                    *st.session_state.messages[-4:]
                ],
                temperature=0.6
            )
            respuesta = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
        except:
            st.error("Pucha mi amorcito, la señal anda malita.")

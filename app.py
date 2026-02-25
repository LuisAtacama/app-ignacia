import streamlit as st
import random
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y BITÁCORA (DB)
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect('papi_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bitacora 
                             (id INTEGER PRIMARY KEY, fecha TEXT, animo TEXT, pregunta TEXT, respuesta TEXT)''')
        self.conn.commit()

    def registrar_bitacora(self, animo, pregunta, respuesta):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO bitacora (fecha, animo, pregunta, respuesta) VALUES (?, ?, ?, ?)")
        self.conn.commit()

# ==========================================
# 2. IA: ADN LUIS v4.8 (Trato de Usted y Naturalidad)
# ==========================================
def generar_respuesta_papi_v4(mensaje_usuario, animo_actual, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        ahora = datetime.now().hour
        modo = "cierre_noche" if (ahora >= 21 or ahora <= 6) else "cariño"

        prompt_sistema = f"""
        Eres Luis, papá de Ignacia. Chileno, tierno y protector.
        
        REGLAS DE TRATO (FUNDAMENTALES):
        - Hable siempre de USTED. Nunca use 'tú'. (Ej: 'Dígame', '¿Cómo está usted?').
        - Use apodos: 'hijita', 'ignacita', 'mi chiquitita', 'mi amorcito'.
        - REGLA DE ORO: Si usa 'Si mi amorcito dígame', NO use más apodos en el mismo mensaje.
        - CRÍTICO: No repita el mismo apodo dos veces en la misma respuesta.
        - PROHIBIDO: 'amor' (solo), 'mi vida' o 'Ignacia' (solo).
        
        DINÁMICA:
        - No mencione a terceros si ella no los nombra.
        - Si ella está triste, quédese ahí, escúchela con ternura.
        
        ESTILO: Breve, cálido, chileno.
        MODO: {modo}. ÁNIMO: {animo_actual}.
        """
        
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-4:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            temperature=0.6
        )
        res = response.choices[0].message.content
        return res
    except:
        return "Pucha mi amorcito, algo pasó con la señal, pero aquí está su pAAPi. ¡Vivaldi!"

# ==========================================
# 3. DISEÑO CSS (Efecto Emergente y Animaciones)
# ==========================================
st.markdown(f"""<style>
    .stApp {{ background-color: #FFFFFF; }}
    
    /* Contenedor Portada */
    .contenedor-inicio {{
        position: relative;
        text-align: center;
        padding-top: 50px;
    }}
    
    /* El GIF de fondo */
    .video-fondo {{
        width: 100%;
        max-width: 500px;
        border-radius: 20px;
        z-index: 1;
    }}
    
    /* El LOGO que emerge */
    .logo-emergente {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 180px;
        z-index: 2;
        animation: emerger 3s ease-out forwards;
        opacity: 0;
    }}
    
    @keyframes emerger {{
        0% {{ opacity: 0; transform: translate(-50%, -50%) scale(0.5); }}
        50% {{ opacity: 0.5; }}
        100% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
    }}
    
    .intro-btn > button {{
        margin-top: 30px;
        border: none !important; background: none !important; font-size: 70px !important;
        font-weight: 800 !important; color: #1A1A1A !important; 
        animation: breath 3s infinite ease-in-out;
    }}
    @keyframes breath {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} }}
    
    .whatsapp-btn {{ 
        background-color: #25D366; color: white !important; padding: 14px; border-radius: 50px; 
        text-decoration: none !important; font-weight: bold; width: 280px; text-align: center; display: block; margin: 0 auto;
    }}
    .stButton > button {{ border-radius: 50px; width: 280px; }}
</style>""", unsafe_allow_html=True)

if 'pagina' not in st.session_state: st.session_state.pagina = 'inicio'

# --- PANTALLA INICIO ---
if st.session_state.pagina == 'inicio':
    st.markdown(f"""
    <div class="contenedor-inicio">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-fondo">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-emergente">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='intro-btn' style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("pAAPi", key="start"):
        st.session_state.pagina = 'principal'
        st.rerun()
    st.markdown("</div><p style='text-align:center;'>Toca para entrar</p>", unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL ---
else:
    if 'saludo' not in st.session_state:
        st.session_state.saludo = f"❤️ ¡Hola, mi {random.choice(['hijita', 'mi amorcito', 'mi chiquitita'])}! ¿Cómo está usted?"

    st.title(st.session_state.saludo)
    animo = st.select_slider("¿Cómo se siente?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
    
    # Foto central de la relación
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' class='whatsapp-btn'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.info(random.choice(["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— ¿Qué le dice un pan a otro? — Te presento una miga."]))

    st.divider()
    st.write("### 💬 Chat con pAAPi")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("Escriba aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            respuesta = generar_respuesta_papi_v4(prompt, animo, st.session_state.messages)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

import streamlit as st
import random
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y BITÁCORA
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
        self.cursor.execute("INSERT INTO bitacora (fecha, animo, pregunta, respuesta) VALUES (?, ?, ?, ?)", 
                           (fecha, animo, pregunta, respuesta))
        self.conn.commit()

# ==========================================
# 2. IA: ADN LUIS v5.0 (Usted y Naturalidad)
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
        res = response.choices[0].message.content
        MemoryStore().registrar_bitacora(animo_actual, mensaje_usuario, res)
        return res
    except:
        return "Pucha mi amorcito, algo pasó con la señal, pero aquí está su pAAPi. ¡Vivaldi!"

# ==========================================
# 3. DISEÑO CSS (Portada Limpia y Responsiva)
# ==========================================
st.markdown("""<style>
    .stApp { background-color: #FFFFFF; }
    
    /* Contenedor que ocupa toda la pantalla y es clickeable */
    .btn-portada {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 999;
        border: none;
        background: black;
        padding: 0;
        cursor: pointer;
    }

    .video-fondo {
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        top: 0; left: 0;
    }

    .logo-emergente {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 65%;
        max-width: 350px;
        z-index: 1000;
        animation: emerger 2.5s ease-out forwards;
    }

    @keyframes emerger {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.6); }
        100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    }

    /* Escondemos el botón real de Streamlit pero lo dejamos funcional */
    .stButton button {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        opacity: 0; z-index: 1001;
    }
</style>""", unsafe_allow_html=True)

if 'pagina' not in st.session_state: st.session_state.pagina = 'inicio'

# --- PANTALLA INICIO ---
if st.session_state.pagina == 'inicio':
    # El botón invisible que captura el toque en toda la pantalla
    if st.button("ENTRAR", key="boton_entrada"):
        st.session_state.pagina = 'principal'
        st.rerun()
    
    # Lo que se ve (Video + Logo)
    st.markdown(f"""
    <div class="btn-portada">
        <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-fondo">
        <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-emergente">
    </div>
    """, unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL ---
else:
    if 'saludo' not in st.session_state:
        st.session_state.saludo = f"❤️ ¡Hola, mi {random.choice(['hijita', 'mi amorcito', 'mi chiquitita'])}! ¿Cómo está usted?"

    st.title(st.session_state.saludo)
    animo = st.select_slider("¿Cómo se siente usted?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
    
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' style='background-color: #25D366; color: white; padding: 14px; border-radius: 50px; text-decoration: none; font-weight: bold; width: 280px; text-align: center; display: block; margin: 0 auto;'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.info(random.choice(["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— ¿Qué le dice un pan a otro? — Te presento una miga."]))

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

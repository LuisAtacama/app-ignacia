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
        self.cursor.execute("INSERT INTO bitacora (fecha, animo, pregunta, respuesta) VALUES (?, ?, ?, ?)", 
                           (fecha, animo, pregunta, respuesta))
        self.conn.commit()

# ==========================================
# 2. IA: ADN LUIS v4.4 (Foco Emocional)
# ==========================================
def generar_respuesta_papi_v4(mensaje_usuario, animo_actual, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        ahora = datetime.now().hour
        modo = "cierre_noche" if (ahora >= 21 or ahora <= 6) else "cariño"

        prompt_sistema = f"""
        Eres Luis, papá de Ignacia. Chileno, tierno y protector.
        
        REGLAS DE ORO DE LENGUAJE:
        - Usa: 'hijita', 'ignacita', 'mi chiquitita' o 'mi amorcito'.
        - Frase de cabecera: 'Si mi amorcito dígame'.
        - PROHIBIDO: 'amor' (a secas), 'mi vida' o 'Ignacia' (a secas).
        
        MANEJO DE CONTEXTO (ESTRICTO):
        - Solo usa los nombres de familiares o amigas (Sofía, Paz, Aída, etc.) si ELLA los nombra primero.
        - NUNCA cambies de tema hacia otras personas para evadir una emoción.
        - Si ella dice que está 'mal' o está triste, QUÉDATE AHÍ. Valida su pena, dile que la entiendes y que estás con ella. No intentes distraerla con temas triviales.
        
        DINÁMICA:
        - Si responde corto ('si', 'mal', 'ya'), no saludes. Responde con profundidad emocional.
        - Ejemplo de respuesta ante 'mal': 'Pucha mi amorcito, me parte el alma que te sientas así. Cuénteme qué tiene, aquí está su pAAPi para escucharla'.
        
        ESTILO: Breve, sentido, chileno ('Vivaldi', 'pucha').
        MODO: {modo}. ÁNIMO ACTUAL: {animo_actual}.
        """
        
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-4:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            temperature=0.7
        )
        res = response.choices[0].message.content
        MemoryStore().registrar_bitacora(animo_actual, mensaje_usuario, res)
        return res
    except:
        return "Pucha mi amorcito, la señal anda malita, pero acá está tu pAAPi. ¡Vivaldi!"

# ==========================================
# 3. DISEÑO Y NAVEGACIÓN (Pantallas)
# ==========================================
st.markdown("""<style>
    .stApp { background-color: #FFFFFF; }
    .button-container { display: flex; flex-direction: column; align-items: center; gap: 15px; margin: 25px 0; }
    .whatsapp-btn { 
        background-color: #25D366; color: white !important; padding: 14px; border-radius: 50px; 
        text-decoration: none !important; font-weight: bold; width: 280px; text-align: center;
    }
    .stButton > button { border-radius: 50px; width: 280px; }
    .intro-btn > button {
        border: none !important; background: none !important; font-size: 80px !important;
        font-weight: 800 !important; color: #1A1A1A !important; animation: breath 3s infinite ease-in-out;
    }
    @keyframes breath { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
</style>""", unsafe_allow_html=True)

# Trazado secreto por URL (?papi=vivaldi)
if st.query_params.get("papi") == "vivaldi":
    with st.sidebar:
        st.success("🕵️ MODO SUPERVISOR")
        db = MemoryStore()
        registros = db.conn.execute("SELECT * FROM bitacora ORDER BY id DESC").fetchall()
        for reg in registros:
            st.info(f"📅 {reg[1]} | 😊 {reg[2]}\n\n**Ella:** {reg[3]}\n\n**Papi:** {reg[4]}")

if 'pagina' not in st.session_state: st.session_state.pagina = 'inicio'

if st.session_state.pagina == 'inicio':
    st.markdown("<div style='height: 25vh;'></div><div class='intro-btn' style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("pAAPi", key="start"):
        st.session_state.pagina = 'principal'
        st.rerun()
    st.markdown("</div><p style='text-align:center;'>Toca para entrar</p>", unsafe_allow_html=True)

else:
    # Pantalla Principal
    if 'saludo' not in st.session_state:
        st.session_state.saludo = f"❤️ ¡Hola, mi {random.choice(['hijita', 'mi amorcito', 'mi chiquitita'])}!"

    st.title(st.session_state.saludo)
    animo = st.select_slider("¿Cómo te sientes?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' class='whatsapp-btn'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.info(random.choice(["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— ¿Qué le dice un pan a otro? — Te presento una miga."]))
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.write("### 💬 Chat con pAAPi")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("Escríbele a pAAPi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            respuesta = generar_respuesta_papi_v4(prompt, animo, st.session_state.messages)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

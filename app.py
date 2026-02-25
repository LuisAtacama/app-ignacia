import streamlit as st
import random
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y BITÁCORA (DB) - REPARADO
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

class MemoryStore:
    def __init__(self):
        # Conexión a la base de datos para el trazado de Don Luis
        self.conn = sqlite3.connect('papi_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # Aseguramos que la tabla de la bitácora exista (reparando lo borrado)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bitacora 
                             (id INTEGER PRIMARY KEY, fecha TEXT, animo TEXT, pregunta TEXT, respuesta TEXT)''')
        self.conn.commit()

    def registrar_bitacora(self, animo, pregunta, respuesta):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO bitacora (fecha, animo, pregunta, respuesta) VALUES (?, ?, ?, ?)", 
                           (fecha, animo, pregunta, respuesta))
        self.conn.commit()

# ==========================================
# 2. IA: ADN LUIS v4.5 (Sin repeticiones)
# ==========================================
def generar_respuesta_papi_v4(mensaje_usuario, animo_actual, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        ahora = datetime.now().hour
        modo = "cierre_noche" if (ahora >= 21 or ahora <= 6) else "cariño"

        prompt_sistema = f"""
        Eres Luis, papá de Ignacia. Chileno, tierno y protector.
        
        REGLAS DE VOCABULARIO (NATURALIDAD):
        - Usa apodos variados: 'hijita', 'ignacita', 'mi chiquitita', 'mi amorcito'.
        - REGLA CRÍTICA: Nunca repitas el mismo apodo dos veces en una sola respuesta.
        - Si usas la frase 'Si mi amorcito dígame', NO agregues ningún otro apodo en el resto del mensaje.
        - PROHIBIDO: 'amor' (solo), 'mi vida' o 'Ignacia' (solo).
        
        MANEJO DE CONTEXTO:
        - Solo nombra a personas (Aída, Sofía, etc.) si ella las menciona primero.
        - Si ella dice que está 'mal', quédate ahí con ella. No cambies de tema.
        
        ESTILO: Breve, cálido, chileno ('Vivaldi', 'pucha'). Habla como un papá, no como un robot.
        MODO: {modo}. ÁNIMO: {animo_actual}.
        """
        
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-4:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            temperature=0.6 # Temperatura más baja para evitar repeticiones robóticas
        )
        res = response.choices[0].message.content
        MemoryStore().registrar_bitacora(animo_actual, mensaje_usuario, res)
        return res
    except:
        return "Pucha mi amorcito, algo pasó con la señal, pero aquí está tu pAAPi. ¡Vivaldi!"

# ==========================================
# 3. DISEÑO CSS
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
        for reg in db.conn.execute("SELECT * FROM bitacora ORDER BY id DESC").fetchall():
            st.info(f"📅 {reg[1]} | 😊 {reg[2]}\n\n**Ella:** {reg[3]}\n\n**Papi:** {reg[4]}")

if 'pagina' not in st.session_state: st.session_state.pagina = 'inicio'

# --- PANTALLA INICIO ---
if st.session_state.pagina == 'inicio':
    st.markdown("<div style='height: 25vh;'></div><div class='intro-btn' style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("pAAPi", key="start"):
        st.session_state.pagina = 'principal'
        st.rerun()
    st.markdown("</div><p style='text-align:center;'>Toca para entrar</p>", unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL ---
else:
    if 'saludo' not in st.session_state:
        st.session_state.saludo = f"❤️ ¡Hola, mi {random.choice(['hijita', 'mi amorcito', 'mi chiquitita'])}!"

    st.title(st.session_state.saludo)
    animo = st.select_slider("¿Cómo te sientes?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
    
    # FOTO
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

    # BOTONES (Chistes y WhatsApp)
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' class='whatsapp-btn'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        chistes = ["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— ¿Qué le dice un pan a otro? — Te presento una miga."]
        st.info(random.choice(chistes))
    st.markdown("</div>", unsafe_allow_html=True)

    # CHAT
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

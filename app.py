import streamlit as st
import random
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y MEMORIA (Bitácora + Episodios)
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect('papi_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # Memoria evolutiva (para que la IA aprenda)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS episodes 
                             (id INTEGER PRIMARY KEY, date TEXT, event TEXT, tags TEXT)''')
        # Bitácora privada para Don Luis
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bitacora 
                             (id INTEGER PRIMARY KEY, fecha TEXT, animo TEXT, pregunta TEXT, respuesta TEXT)''')
        self.conn.commit()

    def registrar_bitacora(self, animo, pregunta, respuesta):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO bitacora (fecha, animo, pregunta, respuesta) VALUES (?, ?, ?, ?)", 
                           (fecha, animo, pregunta, respuesta))
        self.conn.commit()

    def guardar_episodio(self, evento, tags):
        fecha = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO episodes (date, event, tags) VALUES (?, ?, ?)", 
                           (fecha, evento, str(tags)))
        self.conn.commit()

    def obtener_recuerdos(self):
        self.cursor.execute("SELECT event FROM episodes ORDER BY id DESC LIMIT 5")
        return [row[0] for row in self.cursor.fetchall()]

# ==========================================
# 2. MOTOR EMOCIONAL Y CLASIFICADOR
# ==========================================
def clasificar_contexto(texto):
    t = texto.lower()
    tags = []
    if any(k in t for k in ["avión", "vuelo", "viaje", "llegue", "uber"]): tags.append("viaje_transporte")
    if any(k in t for k in ["saqué", "gané", "bien", "7", "logré"]): tags.append("logro")
    if any(k in t for k in ["triste", "miedo", "mal", "lloré", "pelea"]): tags.append("problema")
    if any(k in t for k in ["aída", "mamá", "nona", "tata"]): tags.append("familia_materna")
    return tags

def obtener_estado_emocional(tags):
    # Valores base del Contrato de Estado
    estado = {"ternura": 9, "proteccion": 8, "orgullo": 6, "energia": 7, "modo": "cariño"}
    ahora = datetime.now().hour
    
    if ahora >= 21 or ahora <= 6:
        estado["modo"] = "cierre_noche"
        estado["ternura"] = 10
    elif "viaje_transporte" in tags:
        estado["modo"] = "logistica"
        estado["proteccion"] = 10
    elif "logro" in tags:
        estado["modo"] = "celebracion"
        estado["orgullo"] = 10
    elif "problema" in tags:
        estado["modo"] = "contencion"
        estado["ternura"] = 10
    return estado

# ==========================================
# 3. IA: ADN LUIS v4.0 (Integración Total)
# ==========================================
def generar_respuesta_papi_v4(mensaje_usuario, animo_actual, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        db = MemoryStore()
        
        tags = clasificar_contexto(mensaje_usuario)
        estado = obtener_estado_emocional(tags)
        recuerdos = db.obtener_recuerdos()
        
        # Guardamos el episodio si es relevante
        if tags: db.guardar_episodio(mensaje_usuario, tags)

        prompt_sistema = f"""
        Eres Luis, papá de Ignacia. Chileno, tierno, protector.
        ADN: 'Vivaldi', 'pucha', 'se pasó'. PROHIBIDO: 'mi vida'.
        
        CONTEXTO FAMILIAR:
        - Mamá: Aída (somos equipo, mucho respeto).
        - Familia Paterna: Tío Tomás (Barcelona/Gudslip), Tatis Taimes y Abuelita Marta (la adoraban). Tío Claudio (neutro).
        - Familia Materna: Nona Aída (muy cercana), Tata Ignacio, Tío Nacho.
        - Amistades: Sofía y Paz (Casa 6), Tío Jean Paul (mago).
        
        ESTADO ACTUAL: {json.dumps(estado)}
        ÁNIMO REPORTADO POR ELLA: {animo_actual}
        RECUERDOS RECIENTES: {recuerdos}
        
        REGLA DE CONTINUIDAD: Si ella responde 'si' o algo corto, no saludes. Profundiza en el tema o pregunta por sus amigas Sofía y Paz.
        """
        
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-4:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            temperature=0.8
        )
        respuesta = response.choices[0].message.content
        db.registrar_bitacora(animo_actual, mensaje_usuario, respuesta)
        return respuesta
    except:
        return "Pucha mi niñita, la señal anda malita, pero acá está tu pAAPi. ¡Vivaldi!"

# ==========================================
# 4. DISEÑO Y NAVEGACIÓN
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

# Acceso Secreto URL: ?papi=vivaldi
if st.query_params.get("papi") == "vivaldi":
    with st.sidebar:
        st.success("🕵️ MODO SUPERVISOR")
        db = MemoryStore()
        for reg in db.cursor.execute("SELECT * FROM bitacora ORDER BY id DESC").fetchall():
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
    st.title("❤️ ¡Hola, mi Señora!")
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

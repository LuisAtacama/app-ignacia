import streamlit as st
import random
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y MEMORIA (SQLite)
# ==========================================
st.set_page_config(page_title="Papi Digital - Ignacia Edition", page_icon="🎀", layout="centered")

class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect('papi_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS episodes 
                             (id INTEGER PRIMARY KEY, date TEXT, event TEXT, tags TEXT)''')
        self.conn.commit()

    def add_episode(self, event, tags):
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute("INSERT INTO episodes (date, event, tags) VALUES (?, ?, ?)", 
                           (date, event, str(tags)))
        self.conn.commit()

    def get_recent(self):
        self.cursor.execute("SELECT event FROM episodes ORDER BY id DESC LIMIT 3")
        return [row[0] for row in self.cursor.fetchall()]

# ==========================================
# 2. MOTOR EMOCIONAL CON RUTINA HORARIA
# ==========================================
class EmotionEngine:
    def __init__(self):
        if 'state' not in st.session_state:
            st.session_state.state = {
                "mode": "cariño",
                "emotion": {"ternura": 9, "proteccion": 8, "orgullo": 6, "humor": 6, "estructura": 6, "ansiedad_suave": 2, "energia": 7, "poesia": 5}
            }

    def update_by_context(self, tags):
        s = st.session_state.state
        ahora = datetime.now().hour
        
        if ahora >= 21 or ahora <= 6:
            s["mode"] = "cierre_noche"
            s["emotion"]["ternura"] = 10
            s["emotion"]["energia"] = 3
            s["emotion"]["poesia"] = 8
        elif "viaje_transporte" in tags:
            s["mode"] = "logistica"
            s["emotion"]["proteccion"] += 2
        elif "logro" in tags:
            s["mode"] = "celebracion"
            s["emotion"]["orgullo"] += 3
        elif "problema" in tags:
            s["mode"] = "contencion"
            s["emotion"]["ternura"] += 2
        
        for k in s["emotion"]:
            s["emotion"][k] = max(0, min(10, s["emotion"][k]))

def classify_context(text):
    t = text.lower()
    tags = []
    if any(k in t for k in ["avión", "vuelo", "bus", "llegue", "uber", "furgón"]): tags.append("viaje_transporte")
    if any(k in t for k in ["saqué", "gané", "logré", "7", "6", "bien"]): tags.append("logro")
    if any(k in t for k in ["triste", "miedo", "mal", "lloré", "pelea"]): tags.append("problema")
    if any(k in t for k in ["noche", "dormir", "sueño", "chao"]): tags.append("cierre_noche")
    return tags

# ==========================================
# 3. GENERADOR ADN v2.0
# ==========================================
def generar_respuesta_papi_v2(mensaje_usuario):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        tags = classify_context(mensaje_usuario)
        
        engine = EmotionEngine()
        engine.update_by_context(tags)
        
        db = MemoryStore()
        recuerdos = db.get_recent()
        if tags: db.add_episode(mensaje_usuario, tags)

        prompt_sistema = f"""
        Eres Luis, el papá real de Ignacia. Chileno, tierno y protector.
        MODO ACTUAL: {st.session_state.state['mode']}
        ADN:
        - Usa diminutivos ('hijita', 'niñita').
        - Si el modo es 'cierre_noche': Sé muy dulce, desea dulces sueños, di que descanse.
        - Si el modo es 'celebracion': ¡Siiiii! ¡Esoooo! Qué orgullo.
        - Errores humanos: Alguna letra alargada ('Aaaa que biennnn').
        - RECUERDOS RECIENTES: {recuerdos}
        - ESTADO EMOCIONAL: {json.dumps(st.session_state.state['emotion'])}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": mensaje_usuario}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except:
        return "Pucha mi chiquitita, la señal anda malita, pero te amo infinito. ¡Vivaldi siempre!"

# ==========================================
# 4. INTERFAZ (UI) - DISEÑO MEJORADO
# ==========================================
st.markdown("""<style>
    .stApp { background-color: #FFFFFF; }
    h1 { text-align: center; color: #1a1a1a; font-weight: 700; margin-bottom: 0px; }
    h3 { text-align: center; color: #4a4a4a; margin-top: 10px; }
    
    /* Contenedor de botones centrados */
    .button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 12px; /* Separación leve entre botones */
        margin: 25px 0;
    }
    
    .whatsapp-btn { 
        background-color: #25D366; 
        color: white !important; 
        padding: 14px 30px; 
        border-radius: 50px; 
        text-decoration: none !important; 
        font-weight: bold; 
        display: inline-flex; 
        align-items: center; 
        gap: 10px;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.2);
    }

    /* Estilo para el botón de Streamlit para que parezca el de la captura */
    .stButton > button {
        display: block;
        margin: 0 auto;
        border-radius: 50px;
        padding: 10px 30px;
        border: 1px solid #ddd;
        background-color: white;
        color: #1a1a1a;
        font-size: 16px;
    }
    
</style>""", unsafe_allow_html=True)

if 'palabra_dia' not in st.session_state:
    st.session_state.palabra_dia = random.choice(["Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", "Chiquitita"])

st.title(f"❤️ ¡Hola, mi Señora {st.session_state.palabra_dia}!")

# FOTO Y ÁNIMO
st.write("### 📸 Un recuerdo para hoy")
animo = st.select_slider("¿Cómo te sientes?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
urls_fotos = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"]
st.image(random.choice(urls_fotos), use_container_width=True)

# --- SECCIÓN DE BOTONES CENTRADOS (Uno sobre otro) ---
st.markdown("<div class='button-container'>", unsafe_allow_html=True)

# Botón WhatsApp
st.markdown(f"""
    <a href='https://wa.me/56992238085' class='whatsapp-btn'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='22'>
        HABLAR CON PAPI REAL
    </a>
""", unsafe_allow_html=True)

# Botón Chiste (Streamlit maneja el evento de click)
if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
    st.session_state.mostrar_chiste = True
else:
    if "mostrar_chiste" not in st.session_state:
        st.session_state.mostrar_chiste = False

st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.mostrar_chiste:
    st.info(random.choice(["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— ¿Qué le dice un pan a otro? — Te presento una miga."]))
    st.session_state.mostrar_chiste = False

# CHAT EVOLUTIVO
st.divider()
st.write("### 💬 Chat con pAAPi") # Cambio de texto solicitado

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if prompt := st.chat_input("Escríbele a pAAPi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        respuesta = generar_respuesta_papi_v2(prompt)
        st.write(respuesta)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

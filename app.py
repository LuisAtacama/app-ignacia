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
# 2. IA Y PERSONALIDAD
# ==========================================
def generar_respuesta_papi_v2(mensaje_usuario):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        db = MemoryStore()
        recuerdos = db.get_recent()
        ahora = datetime.now().hour
        modo = "cierre_noche" if (ahora >= 21 or ahora <= 6) else "cariño"

        prompt_sistema = f"""
        Eres Luis, el papá de Ignacia. Chileno, tierno, protector.
        MODO ACTUAL: {modo}. RECUERDOS: {recuerdos}.
        ADN: Usa diminutivos ('hijita'), celebra logros, valida emociones.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": mensaje_usuario}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except:
        return "Pucha mi chiquitita, algo pasó con la señal, pero te amo infinito. ¡Vivaldi!"

# ==========================================
# 3. DISEÑO CSS AVANZADO (PANTALLA INICIO)
# ==========================================
st.markdown("""<style>
    /* Fondo de la app */
    .stApp { background-color: #FFFFFF; }

    /* Pantalla de Inicio Centrada */
    .intro-full {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 70vh;
        text-align: center;
    }

    /* Estilo del texto/botón pAAPi */
    .paapi-logo {
        font-family: 'Inter', sans-serif;
        font-size: 80px;
        font-weight: 800;
        color: #1A1A1A;
        letter-spacing: -2px;
        cursor: pointer;
        transition: all 0.5s ease;
        animation: breath 3s infinite ease-in-out;
        user-select: none;
    }

    @keyframes breath {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    /* Contenedor de botones principales */
    .button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        margin: 30px 0;
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
        width: 280px; 
        justify-content: center;
    }

    .stButton > button {
        display: block;
        margin: 0 auto;
        border-radius: 50px;
        padding: 10px 30px;
        border: 1px solid #ddd;
        background-color: white;
        color: #1a1a1a;
        width: 280px;
    }
</style>""", unsafe_allow_html=True)

# ==========================================
# 4. LÓGICA DE NAVEGACIÓN
# ==========================================
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'

# --- PANTALLA DE INICIO ---
if st.session_state.pagina == 'inicio':
    st.markdown("<div class='intro-full'>", unsafe_allow_html=True)
    
    # El texto pAAPi actúa como botón
    if st.button("pAAPi", key="btn_inicio", help="Toca para entrar"):
        st.session_state.pagina = 'principal'
        st.rerun()
    
    # Sobrescribimos el estilo del botón específico de inicio para que parezca solo texto
    st.markdown("""<style>
        div.stButton > button[kind="secondary"] {
            border: none !important;
            background: none !important;
            font-size: 80px !important;
            font-weight: 800 !important;
            color: #1A1A1A !important;
            height: auto !important;
            width: auto !important;
            animation: breath 3s infinite ease-in-out;
        }
        div.stButton > button:hover { color: #FF4B4B !important; }
    </style>""", unsafe_allow_html=True)
    
    st.write("Toca para entrar")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL ---
else:
    if 'palabra_dia' not in st.session_state:
        st.session_state.palabra_dia = random.choice(["Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente"])

    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.palabra_dia}!")

    # FOTO Y ÁNIMO
    st.write("### 📸 Un recuerdo para hoy")
    animo = st.select_slider("¿Cómo te sientes?", options=["MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"], value="NORMAL")
    urls_fotos = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"]
    st.image(random.choice(urls_fotos), use_container_width=True)

    # BOTONES
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' class='whatsapp-btn'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='22'>HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.session_state.mostrar_chiste = True
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get('mostrar_chiste'):
        st.info(random.choice(["— ¿Cómo se llama el campeón japonés de buceo? — Tokofondo.", "— Robinson Crusoe y lo atropellaron."]))
        st.session_state.mostrar_chiste = False

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
            respuesta = generar_respuesta_papi_v2(prompt)
            st.write(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Botón discreto para volver
    if st.sidebar.button("🏠 Salir"):
        st.session_state.pagina = 'inicio'
        st.rerun()

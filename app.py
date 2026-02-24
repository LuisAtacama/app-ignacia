import streamlit as st
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container { background-color: #FFFFFF; padding: 40px !important; max-width: 600px; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #1A1A1A !important; text-align: center; }
    .frase-papi { text-align: center; font-style: italic; font-size: 19px; color: #1A1A1A; margin-top: 20px; padding: 15px; border-top: 1px solid #EEE; }
    .chiste-box { background-color: #F0F2F6; border-radius: 15px; padding: 20px; text-align: center; font-size: 18px; color: #1A1A1A; margin: 20px 0; border: 1px dashed #CCC; }
    .whatsapp-btn { background-color: #25D366; color: white !important; padding: 16px 32px; border-radius: 50px; text-decoration: none !important; font-weight: 700; display: inline-flex; align-items: center; gap: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DATOS EMPAREJADO (FOTO + SU TEXTO) ---
galeria_maestra = [
    {"url": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "txt": "Este abrazo me lo guardo en el corazón para siempre. Usted sabe que papi está ahí con usted."},
    {"url": "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "txt": "¡Mire qué carita de felicidad con su oso! Esa alegría suya es lo más importante del mundo."},
    {"url": "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "txt": "¡Aaaaa pero qué estilosa! Me encanta verla así de canchera, tiene un gusto excelente."},
    {"url": "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "txt": "Ahí se ve muy tranquila y valiente. Acuérdese que usted es súper inteligente."},
    {"url": "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "txt": "Pucha que lo pasamos bacán ese día. Me pone muy feliz recordarlo."},
    {"url": "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "txt": "¡Qué buena foto! Se ve muy despierta, así la quiero: ¡Vivaldi siempre!"},
    {"url": "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "txt": "Usted tiene una luz especial. Nunca olvide que no hay nada que cambiar en usted."},
    {"url": "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "txt": "¡Esa es mi artista favorita! Tiene un ojo increíble para capturar momentos."},
    {"url": "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "txt": "Linda mi chiquitita. Aquí estoy atento a lo que necesite siempre."},
    {"url": "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "txt": "¡Aaaaa qué hermosa se ve! Me hace sentir el papá más orgulloso del universo."}
    # ... (puede seguir agregando las 50 fotos aquí siguiendo este formato)
]

# --- 3. BANCO DE CHISTES ---
chistes = [
    "— ¡Papá, papá! ¿Te gusta el café? \n — Sí, ¿por qué? \n — ¡Porque acabo de tirar tu taza favorita!",
    "— Jaimito, ¿qué es la 'A'? \n — Una vocal, profesora. \n — ¿Y la 'K'? \n — ¡Una letra que no se puede comer!",
    "— ¿Cómo se dice 'pobre' en chino? \n — Chin-un-p... (¡No sea mal pensado hijita, es Chin-din-elo!)",
    "— ¿Cuál es el último animal que subió al arca de Noé? \n — ¡El del-fín!",
    "— ¿Qué le dice un jaguar a otro jaguar? \n — Jaguar you?"
]

# --- 4. ESTRUCTURA APP ---
st.title("❤️ Hola, Ignacita linda")

# SECCIÓN FOTOS
st.write("### 📸 Un recuerdo para hoy")
animo = st.select_slider(label="¿Cómo se siente?", options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"])

if animo != "Seleccione":
    recuerdo = random.choice(galeria_maestra)
    st.image(recuerdo["url"], use_container_width=True)
    st.markdown(f'<p class="frase-papi">"{recuerdo["txt"]}"</p>', unsafe_allow_html=True)
else:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

st.divider()

# SECCIÓN CHISTES
st.write("### 🤡 ¡Un chiste para alegrar el día!")
if st.button("¡Cuéntame un chiste, Papi!"):
    chiste_hoy = random.choice(chistes)
    st.markdown(f'<div class="chiste-box">{chiste_hoy}</div>', unsafe_allow_html=True)
    st.write("¡Jajaja! Estemos Vivaldi con la alegría siempre.")

# WhatsApp
st.markdown("""<div style='text-align:center; margin-top:50px;'><a href='https://wa.me/56992238085' class='whatsapp-btn'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='26'> HABLAR CON PAPI</a></div>""", unsafe_allow_html=True)

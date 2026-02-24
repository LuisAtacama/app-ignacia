import streamlit as st
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- DISEÑO CSS (PULCRO, MÍNIMO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container { background-color: #FFFFFF; padding: 40px !important; font-family: 'Inter', sans-serif; max-width: 600px; }
    h1 { color: #1A1A1A !important; font-weight: 700; font-size: 32px; text-align: center; }
    h3 { color: #4A4A4A !important; font-weight: 400; font-size: 18px; text-align: center; margin-bottom: 30px; }
    .frase-papi { text-align: center; font-style: italic; font-size: 19px; color: #1A1A1A; margin-top: 20px; padding: 15px; line-height: 1.5; }
    .whatsapp-container { text-align: center; margin-top: 50px; }
    .whatsapp-btn { background-color: #25D366; color: white !important; padding: 16px 32px; border-radius: 50px; text-decoration: none !important; font-weight: 700; display: inline-flex; align-items: center; gap: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE RECUERDOS (FOTO + TEXTO PERSONALIZADO) ---
# He seleccionado algunas de sus fotos con textos que siguen su ADN
recuerdos = [
    {"url": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "texto": "Este abrazo lo guardo siempre conmigo. Usted es mi mayor orgullo, mi niñita linda."},
    {"url": "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "texto": "¡Mire qué carita de felicidad! Nunca pierda esa sonrisa, que ilumina todo."},
    {"url": "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "texto": "¡Aaaa que bien se ve ahí! Siempre con su estilo único, se pasó de artista."},
    {"url": "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "texto": "Usted es una niña muy inteligente y valiente. ¡Acuérdese siempre de eso!"},
    {"url": "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "texto": "Pucha que lo pasamos bacán ese día. Me encanta verla disfrutar así."},
    {"url": "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "texto": "Ahí estaba bien Vivaldi, ¡como tiene que ser siempre mi chiquitita!"},
    {"url": "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "texto": "Cada vez que vea esta foto, recuerde que papi está al ladito suyo en el corazón."},
    {"url": "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "texto": "Usted tiene un gusto excelente. ¡Esa es mi artista favorita!"},
    {"url": "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "texto": "No hay nada que cambiar en usted, hijita linda. Es perfecta tal como es."},
    {"url": "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "texto": "¡Se pasó de linda! Le mando un abrazo apretado desde acá."},
    {"url": "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png", "texto": "¡Qué buen recuerdo! Estemos siempre Vivaldi con la alegría, ¿ya?"}
]

# --- 3. ESTRUCTURA APP ---
st.title("❤️ Hola, Ignacita linda")
st.write("### ¿Cómo se siente usted hoy?")

animo = st.select_slider(
    label="",
    options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"]
)

st.divider()

if animo != "Seleccione":
    # Selecciona un recuerdo completo (Foto + Su texto específico)
    recuerdo_hoy = random.choice(recuerdos)
    st.image(recuerdo_hoy["url"], use_container_width=True)
    
    # El texto personalizado de la foto
    st.markdown(f'<p class="frase-papi">"{recuerdo_hoy["texto"]}"</p>', unsafe_allow_html=True)
    
    if animo in ["FELIZ", "MUY FELIZ"]:
        st.balloons()
else:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    st.markdown('<p class="frase-papi">Mueva la barra de arriba para ver algo que le preparé...</p>', unsafe_allow_html=True)

# --- 4. ACCESO DIRECTO ---
st.markdown(f"""
    <div class="whatsapp-container">
        <a href="https://wa.me/56992238085" class="whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="26">
            HABLAR CON PAPI
        </a>
    </div>
""", unsafe_allow_html=True)

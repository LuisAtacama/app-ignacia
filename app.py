import streamlit as st
import random
from openai import OpenAI

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- CONEXIÓN A IA (SECRETS) ---
# El bloque try/except es para que la app no se caiga si la llave falla
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Error técnico: No se encontró la API KEY en los Secrets.")

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container { background-color: #FFFFFF; padding: 40px !important; max-width: 650px; font-family: 'Inter', sans-serif; }
    h1 { color: #1A1A1A !important; text-align: center; font-weight: 700; }
    .mensaje-animo { text-align: center; font-size: 20px; color: #1A1A1A; font-style: italic; margin-top: 20px; padding: 10px; border-top: 1px solid #EEE; }
    .chiste-box { background-color: #F8F9FA; border-radius: 15px; padding: 25px; text-align: center; font-size: 18px; border: 1px solid #EEE; line-height: 1.6; white-space: pre-wrap; }
    .whatsapp-btn { background-color: #25D366; color: white !important; padding: 16px 32px; border-radius: 50px; text-decoration: none !important; font-weight: 700; display: inline-flex; align-items: center; gap: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- ADN LUIS ---
ADN_LUIS = """
Eres Luis, papá chileno de Ignacia. Eres cariñoso, protector y orgulloso.
Usa palabras como: 'bacán', 'se pasó', 'Pucha', 'Vivaldi', 'mi chiquitita', 'hijita linda'.
Responde siempre en 1 o 2 frases cortas. Valida su emoción con amor.
"""

# --- LISTADOS ---
palabras = ["Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"]

urls_fotos = [
    "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg",
    "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg",
    "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg",
    "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg",
    "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg",
    "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg",
    "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg",
    "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg",
    "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg",
    "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg",
    "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg",
    "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg",
    "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg",
    "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg",
    "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg",
    "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg",
    "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg",
    "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg",
    "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg",
    "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg",
    "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg",
    "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg",
    "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg",
    "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg",
    "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"
]

chistes_reales = ["— En Hawai uno no se hospeda, se aloha.", "— ¿Cómo se llama el campeón japonés de buceo?\n— Tokofondo.\n— ¿Y el segundo lugar?\n— Kasitoko.", "— Ayer pasé por tu casa y me tiraste una palta… qué palta de respeto.", "— Robinson Crusoe y lo atropellaron.", "— El otro día vi a un otaku triste y lo animé.", "— Ayer metí un libro de récords en la batidora y batí todos los récords.", "— ¿Qué le dice un pan a otro pan?\n— Te presento una miga.", "— Cuando estés triste abraza un zapato.\n— Un zapato consuela.", "— Doctor, doctor, tengo un hueso afuera.\n— ¡Hágalo pasar!", "— Una señora llorando llega a una zapatería:\n— ¿Tiene zapatos de cocodrilo?\n— ¿Qué número calza su cocodrilo?", "— Un tipo va al oculista.\n— Mire la pared.\n— ¿Cuál pared?", "— Un español le pregunta a un inglés:\n— ¿Cómo llaman a los bomberos?\n— Firemen.\n— Nosotros los llamamos por teléfono.", "— ¿Te sabes el chiste del tarro?\n— No.\n— ¡Qué lata!", "— Tengo un perro que dice “Hola”.\n— En mi casa tengo un tarro que dice “Nescafé”.", "— ¿Aló, está Joaco?\n— No, Joaco mprar.", "— ¿Qué le dijo un techo a otro techo?\n— Techo de menos.", "— ¿Qué hace una abeja en el gimnasio?\n— Zum-ba.", "— Te haré una última pregunta. Si la sabes, te apruebo.\n¿Cuántos pelos tiene la cola de un caballo?\n— 30.583.\n— ¿Y cómo lo sabes?\n— Perdone profesor… pero esa ya es otra pregunta."]

# --- MOTOR DE IA ---
def generar_respuesta_ia(animo_texto, historial):
    try:
        mensajes = [{"role": "system", "content": ADN_LUIS}]
        for m in historial[-5:]:
            mensajes.append(m)
        mensajes.append({"role": "user", "content": f"Me siento {animo_texto}. Dime algo como mi papá Luis."})
        
        # Cambiamos a la función de chat más estable
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            max_tokens=100
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Esto solo saldrá si la API realmente falla
        return f"Pucha mi chiquitita, aquí está tu papi. No te preocupes, todo va a estar bien. ¡Vivaldi siempre!"

# --- INICIO APP ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

palabra_del_dia = random.choice(palabras)
st.title(f"❤️ ¡Hola, mi Señora {palabra_del_dia}!")

st.write("### 📸 Un recuerdo para hoy")
animo = st.select_slider(label="¿Cómo se siente?", options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"])

st.divider()

if animo != "Seleccione":
    st.image(random.choice(urls_fotos), use_container_width=True)
    with st.spinner("Papi está escribiendo..."):
        respuesta = generar_respuesta_ia(animo, st.session_state.chat_history)
        st.markdown(f'<div class="mensaje-animo">{respuesta}</div>', unsafe_allow_html=True)
    if animo in ["FELIZ", "MUY FELIZ"]: st.balloons()
else:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

# CHAT
st.divider()
st.write("### 💬 Chat con Papi")
for m in st.session_state.chat_history:
    with st.chat_message(m["role"]): st.write(m["content"])

user_input = st.chat_input("Escribe aquí...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        reply = generar_respuesta_ia(user_input, st.session_state.chat_history)
        st.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# CHISTES Y WHATSAPP
st.divider()
if st.button("🤡 ¡Cuéntame un chiste, Papi!"):
    st.markdown(f'<div class="chiste-box">{random.choice(chistes_reales)}</div>', unsafe_allow_html=True)

st.markdown("""<div style='text-align:center; margin-top:50px;'><a href='https://wa.me/56992238085' class='whatsapp-btn'>HABLAR CON PAPI REAL</a></div>""", unsafe_allow_html=True)

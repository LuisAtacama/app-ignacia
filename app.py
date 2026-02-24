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
    h1 { color: #1A1A1A !important; text-align: center; font-weight: 700; }
    h3 { color: #4A4A4A !important; text-align: center; }
    .chiste-box { background-color: #F8F9FA; border-radius: 15px; padding: 25px; text-align: center; font-size: 18px; color: #1A1A1A; margin: 20px 0; border: 1px solid #EEE; line-height: 1.6; white-space: pre-wrap; }
    .whatsapp-btn { background-color: #25D366; color: white !important; padding: 16px 32px; border-radius: 50px; text-decoration: none !important; font-weight: 700; display: inline-flex; align-items: center; gap: 12px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LISTADO DE PALABRAS PERSONALIZADAS ---
palabras = [
    "Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", 
    "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", 
    "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", 
    "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"
]

# --- 3. INICIO: SALUDO DINÁMICO ---
palabra_del_dia = random.choice(palabras)
st.title(f"❤️ ¡Hola, mi Señora {palabra_del_dia}!")

# --- 4. LISTA DE FOTOS ---
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

# --- 5. BANCO DE CHISTES (NUEVA LISTA DE IMAGEN) ---
chistes_reales = [
    "1. — En Hawai uno no se hospeda, se aloha.",
    "2. — ¿Cómo se llama el campeón japonés de buceo?\n— Tokofondo.\n— ¿Y el segundo lugar?\n— Kasitoko.",
    "3. — Ayer pasé por tu casa y me tiraste una palta… qué palta de respeto.",
    "4. — Robinson Crusoe y lo atropellaron.",
    "5. — El otro día vi a un otaku triste y lo animé.",
    "6. — Ayer metí un libro de récords en la batidora y batí todos los récords.",
    "7. — ¿Qué le dice un pan a otro pan?\n— Te presento una miga.",
    "8. — Cuando estés triste abraza un zapato.\n— Un zapato consuela.",
    "9. — Doctor, doctor, tengo un hueso afuera.\n— ¡Hágalo pasar!",
    "10. — Una señora llorando llega a una zapatería:\n— ¿Tiene zapatos de cocodrilo?\n— ¿Qué número calza su cocodrilo?",
    "11. — Un tipo va al oculista.\n— Mire la pared.\n— ¿Cuál pared?",
    "12. — Un español le pregunta a un inglés:\n— ¿Cómo llaman a los bomberos?\n— Firemen.\n— Nosotros los llamamos por teléfono.",
    "13. — ¿Te sabes el chiste del tarro?\n— No.\n— ¡Qué lata!",
    "14. — Tengo un perro que dice “Hola”.\n— En mi casa tengo un tarro que dice “Nescafé”.",
    "15. — ¿Aló, está Joaco?\n— No, Joaco mprar.",
    "16. — ¿Qué le dijo un techo a otro techo?\n— Techo de menos.",
    "17. — ¿Qué hace una abeja en el gimnasio?\n— Zum-ba.",
    "18. — Te haré una última pregunta. Si la sabes, te apruebo.\n¿Cuántos pelos tiene la cola de un caballo?\n— 30.583.\n— ¿Y cómo lo sabes?\n— Perdone profesor… pero esa ya es otra pregunta."
]

# --- 6. CUERPO DE LA APP ---
st.write("### 📸 Un recuerdo para hoy")
animo = st.select_slider(label="¿Cómo se siente?", options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"])

st.divider()

if animo != "Seleccione":
    foto_elegida = random.choice(urls_fotos)
    st.image(foto_elegida, use_container_width=True)
    if animo in ["FELIZ", "MUY FELIZ"]: 
        st.balloons()
else:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

st.divider()

st.write("### 🤡 ¡Un chiste para alegrar el día!")
if st.button("¡Cuéntame un chiste, Papi!"):
    chiste_hoy = random.choice(chistes_reales)
    st.markdown(f'<div class="chiste-box">{chiste_hoy}</div>', unsafe_allow_html=True)

# WhatsApp
st.markdown("""<div style='text-align:center; margin-top:50px;'><a href='https://wa.me/56992238085' class='whatsapp-btn'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='26'> HABLAR CON PAPI</a></div>""", unsafe_allow_html=True)

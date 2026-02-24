import streamlit as st
import random

# 1. Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- DISEÑO MODERNO: BOTONES REDONDOS Y LETRAS BLANCAS ---
foto_fondo = "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    .stApp {{
        background-image: url("{foto_fondo}");
        background-attachment: fixed;
        background-size: cover;
    }}
    
    /* Capa oscura para que las letras blancas resalten */
    .main {{
        background-color: rgba(0, 0, 0, 0.6); 
        padding: 30px;
        border-radius: 20px;
        margin: 10px;
        font-family: 'Inter', sans-serif;
    }}

    /* Todo el texto de la app en BLANCO */
    h1, h2, h3, p, span, label, .stMarkdown, .stSubheader {{
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}

    /* Estilo de BOTONES REDONDOS BLANCOS SÓLIDOS */
    div.stButton > button {{
        width: 100px;
        height: 100px;
        border-radius: 50% !important; /* Totalmente redondos */
        background-color: #FFFFFF !important; /* Blanco Sólido */
        color: #333333 !important; /* Letra oscura dentro del botón para leer el emoji/texto */
        border: none;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    
    div.stButton > button:hover {{
        transform: scale(1.1);
        background-color: #f0f0f0 !important;
    }}

    /* Caja de chistes con fondo traslúcido y letra blanca */
    .stInfo {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
    }}

    /* Botón WhatsApp: MENSAJE A PAPI */
    .papi-btn {{
        background-color: #25D366;
        color: white !important;
        padding: 18px 35px;
        border-radius: 50px;
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        font-weight: bold;
        letter-spacing: 1px;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DATOS ---
fotos_galeria = [
    "https://i.postimg.cc/26433cj7/IMG-5004.jpg", "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg",
    "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "https://i.postimg.cc/dV17njnY/IMG-5047.jpg",
    "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg",
    "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg",
    "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg",
    "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "https://i.postimg.cc/7hnCtBpw/IMG-5099.jpg",
    "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "https://i.postimg.cc/rmWRxyjg/IMG-5114.jpg",
    "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "https://i.postimg.cc/0QmKD5nM/IMG-5119.jpg",
    "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/s2bZMGYS/IMG-5137.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg",
    "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "https://i.postimg.cc/6Q8v6fvK/IMG-5200.jpg",
    "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg",
    "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/g2ShPTr6/IMG-5254.jpg",
    "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg",
    "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg",
    "https://i.postimg.cc/fTsm7d6M/IMG-5315.jpg", "https://i.postimg.cc/fWmY0CgL/IMG-5316.jpg", "https://i.postimg.cc/8kMLr4nk/IMG-5317.jpg",
    "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg",
    "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg",
    "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg",
    "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg"
]

lista_chistes = [
    "— En Hawai uno no se hospeda, se aloha.", "— ¿Cómo se llama el campeón japonés de buceo? Tokofondo. ¿Y el segundo? Kasitoko.",
    "— Ayer pasé por su casa y me tiró una palta… qué palta de respeto.", "— Robinson Crusoe y lo atropellaron.",
    "— El otro día vi a un otaku triste y lo animé.", "— Ayer metí un libro de récords en la batidora y batí todos los récords.",
    "— ¿Qué le dice un pan a otro pan? Le presento una miga.", "— Cuando esté triste abraza un zapato. Un zapato consuela.",
    "— Doctor, doctor, tengo un hueso afuera. ¡Hágalo pasar!", "— Una señora llorando llega a una zapatería: ¿Tiene zapatos de cocodrilo? ¿Qué número calza su cocodrilo?",
    "— Había una vez un niñito llamado Nintendo, lo atropellaron y dijo: Game Over.", "— Un tipo va al oculista. —Mire la pared. —¿Cuál pared?",
    "— ¿Cómo se llama su padre? —Igual. —¿Don Igual? —Sí.", "— Un español le pregunta a un inglés: Firemen. —Nosotros por teléfono.",
    "— ¿Se sabe el chiste del tarro? —No. —¡Qué lata!", "— Había un niñito que se llamaba Tarea. Tarea para la casa. Y Tarea se fue.",
    "— Tengo un perro que dice “Hola”. —En mi casa tengo un tarro que dice “Nescafé”.", "— ¿Qué le dijo un poste de luz a otro? El último apaga la luz.",
    "— ¿Aló, está Joaco? —No, Joaco Imprar.", "— Señorita, ¿hayalletas? (Hay galletas)",
    "— ¿Cómo estornuda un tomate? ¡Ketchup!", "— ¿Qué le dijo un árbol a otro? Nos dejaron plantados.",
    "— ¿Qué le dijo un techo a otro? Techo de menos.", "— ¿Qué hace una abeja en el gimnasio? Zum-ba.",
    "— Robinson Crusoe… quedó solo.", "— ¿Cuántos pelos tiene la cola de un caballo? 30.583. ¿Y cómo lo sabe? Esa es otra pregunta."
]

# --- 3. LÓGICA ---
if 'saludo' not in st.session_state:
    st.session_state.saludo = random.choice(["Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"])

# --- 4. INTERFAZ ---
st.title(f"❤️ ¡Hola, mi Señora {st.session_state.saludo}!")
st.subheader("¿Cómo se siente usted hoy?")

# Botones en 2 filas y 2 columnas, bien centrados
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

opcion = None

with col1:
    if st.button("😔"): opcion = "Triste"
with col2:
    if st.button("😐"): opcion = "Normal"
with col3:
    if st.button("😊"): opcion = "Feliz"
with col4:
    if st.button("🚀"): opcion = "Súper"

st.markdown("<br>", unsafe_allow_html=True)

if opcion:
    chiste = random.choice(lista_chistes)
    foto = random.choice(fotos_galeria)
    
    if opcion == "Triste":
        st.write("### Mi niñita, un chiste fome para alegrar el día:")
    elif opcion == "Normal":
        st.write("### ¡Disfrute su día! Aquí uno quizás no tan fome:")
    else:
        st.write("### ¡Esa es mi hija! ¡A celebrar!")
        st.balloons()
        if opcion == "Súper": st.snow()
    
    st.info(chiste)
    st.image(foto, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center;">
        <a href="https://wa.me/56992238085" class="papi-btn">
            MENSAJE A PAPI
        </a>
    </div>
""", unsafe_allow_html=True)

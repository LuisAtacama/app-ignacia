import streamlit as st
import random

# 1. Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- DISEÑO SOFISTICADO CON FONDO PERSONALIZADO ---
# Usaremos una de sus fotos de fondo con un filtro para que no moleste la lectura
foto_fondo = "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{foto_fondo}");
        background-attachment: fixed;
        background-size: cover;
    }}
    /* Capa de legibilidad: un fondo oscuro semitransparente sobre el fondo */
    .main {{
        background-color: rgba(255, 255, 255, 0.85); /* Blanco traslúcido para que se lea todo */
        padding: 20px;
        border-radius: 20px;
        margin: 10px;
    }}
    /* Títulos con estilo */
    h1 {{
        color: #d63384;
        font-family: 'Georgia', serif;
        text-align: center;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 10px;
    }}
    /* Estilo para los mensajes de chistes */
    .stInfo {{
        border-radius: 15px;
        border-left: 5px solid #d63384;
    }}
    /* Botón de WhatsApp */
    .whatsapp-btn {{
        background-color: #25D366;
        color: white;
        padding: 15px 25px;
        border-radius: 50px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        font-weight: bold;
        gap: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. EL BANCO DE DATOS (FOTOS Y CHISTES) ---

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

palabras = ["Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"]

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

# --- 3. LÓGICA DE MEMORIA (Para chistes y ahora también FOTOS) ---
if 'chistes_vistos' not in st.session_state or len(st.session_state.chistes_vistos) == len(lista_chistes):
    st.session_state.chistes_vistos = []
if 'fotos_vistas' not in st.session_state or len(st.session_state.fotos_vistas) == len(fotos_galeria):
    st.session_state.fotos_vistas = []

chistes_disp = [c for c in lista_chistes if c not in st.session_state.chistes_vistos]
fotos_disp = [f for f in fotos_galeria if f not in st.session_state.fotos_vistas]

chiste_actual = random.choice(chistes_disp)
foto_actual = random.choice(fotos_disp)

if 'saludo' not in st.session_state:
    st.session_state.saludo = random.choice(palabras)

# --- 4. CUERPO DE LA APP ---
st.title(f"❤️ ¡Hola, mi Señora {st.session_state.saludo}!")
st.markdown("<p style='text-align: center;'><b>Dedicado con todo mi amor para usted.</b></p>", unsafe_allow_html=True)

st.subheader("💬 ¿Cómo se siente usted hoy?")
animo = st.select_slider("Deslice la barrita:", options=["Seleccione", "Triste", "Normal", "Feliz", "¡Súper Feliz!"])

st.write("---")

if animo == "Seleccione":
    st.info("✨ Mueva la barrita de arriba para recibir su mensaje, mi niñita.")
else:
    # Registrar lo visto
    st.session_state.chistes_vistos.append(chiste_actual)
    st.session_state.fotos_vistas.append(foto_actual)

    if animo == "Triste":
        st.write("### Mi niñita, un chiste fome para alegrar el día. Mire:")
        st.info(chiste_actual)
        st.image(foto_actual, use_container_width=True)

    elif animo == "Normal":
        st.write("### ¡Disfrute su día! Aquí uno quizás no tan fome:")
        st.info(chiste_actual)
        st.image(foto_actual, use_container_width=True)

    elif animo == "Feliz":
        st.write("### ¡Esa es mi hija! Mire este video:")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.image(foto_actual, caption="¡Usted es pura luz!", use_container_width=True)

    elif animo == "¡Súper Feliz!":
        st.write("### ¡CELEBRACIÓN TOTAL PARA USTED! 🎉")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.snow()
        st.image(foto_actual, use_container_width=True)

    st.write("---")
    # Botón WhatsApp Estilizado
    st.markdown("""
        <div style="text-align: center;">
            <a href="https://wa.me/56992238085" class="whatsapp-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20">
                ENVIARLE UN MENSAJE A PAPÁ
            </a>
        </div>
    """, unsafe_allow_html=True)

import streamlit as st
import random

# 1. Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- DISEÑO: FONDO BLANCO PLANO Y TIPOGRAFÍA MODERNA ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    /* Fondo blanco plano en toda la app */
    .stApp {{
        background-color: #FFFFFF;
    }}
    
    /* Contenedor central limpio */
    .main .block-container {{
        background-color: #FFFFFF;
        padding: 40px !important;
        font-family: 'Inter', sans-serif;
        max-width: 600px;
    }}

    /* Textos en gris oscuro/negro para contraste sobre blanco */
    h1, h3, p, label, .stMarkdown {{
        color: #1A1A1A !important;
        font-family: 'Inter', sans-serif !important;
        text-align: center;
    }}

    h1 {{
        font-weight: 700;
        margin-bottom: 30px;
    }}

    /* Estilo para la barra (Slider) */
    .stSlider {{
        padding-top: 20px;
        padding-bottom: 40px;
    }}

    /* Caja de chistes minimalista */
    .stInfo {{
        background-color: #F8F9FA !important;
        color: #333333 !important;
        border: 1px solid #EEEEEE !important;
        border-radius: 15px;
        padding: 20px !important;
    }}

    /* Botón WhatsApp: Logo + Texto (Sin subrayado) */
    .whatsapp-container {{
        text-align: center;
        margin-top: 40px;
    }}

    .whatsapp-btn {{
        background-color: #25D366;
        color: white !important;
        padding: 16px 32px;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-size: 16px;
        transition: transform 0.2s ease;
    }}
    
    .whatsapp-btn:hover {{
        transform: scale(1.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DATOS ACTUALIZADO ---
fotos_galeria = [
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
st.write("### ¿Cómo se siente usted hoy?")

# BARRA DESLIZANTE CON 5 CLASIFICACIONES
animo = st.select_slider(
    label="Deslice para elegir su estado:",
    options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"]
)

if animo != "Seleccione":
    chiste = random.choice(lista_chistes)
    foto = random.choice(fotos_galeria)
    
    st.info(chiste)
    
    if animo in ["FELIZ", "MUY FELIZ"]:
        st.balloons()
        if animo == "MUY FELIZ":
            st.snow()
    
    st.image(foto, use_container_width=True)

# BOTÓN WHATSAPP LIMPIO
st.markdown(f"""
    <div class="whatsapp-container">
        <a href="https://wa.me/56992238085" class="whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="24" height="24">
            MENSAJE A PAPI
        </a>
    </div>
""", unsafe_allow_html=True)

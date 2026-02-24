import streamlit as st
import random

# 1. Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- DISEÑO SOFISTICADO (CSS) ---
st.markdown("""
    <style>
    /* Cambiar el fondo de la app */
    .stApp {
        background-color: #fdf5f7;
    }
    /* Estilizar los títulos */
    h1 {
        color: #d63384;
        font-family: 'Georgia', serif;
        text-align: center;
    }
    /* Estilizar el cuadro del chiste */
    .stInfo {
        background-color: #ffffff;
        border-left: 5px solid #d63384;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    /* Botón de WhatsApp más elegante */
    div.stButton > button {
        background-color: #25d366;
        color: white;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LISTADOS ---
palabras = [
    "Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", 
    "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", 
    "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", 
    "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"
]

lista_chistes = [
    "— En Hawai uno no se hospeda, se aloha.",
    "— ¿Cómo se llama el campeón japonés de buceo? Tokofondo. ¿Y el segundo? Kasitoko.",
    "— Ayer pasé por su casa y me tiró una palta… qué palta de respeto.",
    "— Robinson Crusoe y lo atropellaron.",
    "— El otro día vi a un otaku triste y lo animé.",
    "— Ayer metí un libro de récords en la batidora y batí todos los récords.",
    "— ¿Qué le dice un pan a otro pan? Le presento una miga.",
    "— Cuando esté triste abraza un zapato. Un zapato consuela.",
    "— Doctor, doctor, tengo un hueso afuera. ¡Hágalo pasar!",
    "— Una señora llorando llega a una zapatería: ¿Tiene zapatos de cocodrilo? ¿Qué número calza su cocodrilo?",
    "— Había una vez un niñito llamado Nintendo, lo atropellaron y dijo: Game Over.",
    "— Un tipo va al oculista. —Mire la pared. —¿Cuál pared?",
    "— ¿Cómo se llama su padre? —Igual. —¿Don Igual? —Sí.",
    "— Un español le pregunta a un inglés: ¿Cómo llaman a los bomberos? —Firemen. —Nosotros por teléfono.",
    "— ¿Te sabes el chiste del tarro? —No. —¡Qué lata!",
    "— Había un niñito que se llamaba Tarea. Tarea para la casa. Y Tarea se fue.",
    "— Tengo un perro que dice “Hola”. —En mi casa tengo un tarro que dice “Nescafé”.",
    "— ¿Qué le dijo un poste de luz a otro? El último apaga la luz.",
    "— ¿Aló, está Joaco? —No, Joaco Imprar.",
    "— Señorita, ¿hayalletas? (Hay galletas)",
    "— ¿Cómo estornuda un tomate? ¡Ketchup!",
    "— ¿Qué le dijo un árbol a otro? Nos dejaron plantados.",
    "— ¿Qué le dijo un techo a otro? Techo de menos.",
    "— ¿Qué hace una abeja en el gimnasio? Zum-ba.",
    "— Robinson Crusoe… quedó solo.",
    "— ¿Cuántos pelos tiene la cola de un caballo? 30.583. ¿Y cómo lo sabe? Esa es otra pregunta."
]

# --- 3. LÓGICA DE MEMORIA ---
if 'chistes_vistos' not in st.session_state or len(st.session_state.chistes_vistos) == len(lista_chistes):
    st.session_state.chistes_vistos = []

chistes_disponibles = [c for c in lista_chistes if c not in st.session_state.chistes_vistos]
chiste_del_momento = random.choice(chistes_disponibles)

if 'saludo' not in st.session_state:
    st.session_state.saludo = random.choice(palabras)

# --- INICIO DE LA APP ---
st.title(f"❤️ ¡Hola, mi Señora {st.session_state.saludo}!")

st.markdown(f"<p style='text-align: center; font-style: italic;'>Dedicado con todo mi amor para usted.</p>", unsafe_allow_html=True)

st.subheader("💬 ¿Cómo se siente usted hoy?")
animo = st.select_slider(
    "Deslice la barrita para que papá le responda:",
    options=["Seleccione", "Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

st.divider()

if animo == "Seleccione":
    st.write("✨ Mueva la barrita de arriba para recibir un mensaje especial...")

else:
    if chiste_del_momento not in st.session_state.chistes_vistos:
        st.session_state.chistes_vistos.append(chiste_del_momento)

    if animo == "Triste":
        st.write("### Mi niñita, un chiste fome para alegrar el día. Mire:")
        st.info(chiste_del_momento)
        st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

    elif animo == "Normal":
        st.write("### ¡Disfrute su día! Aquí otro quizás no tan fome:")
        st.info(chiste_del_momento)
        st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", use_container_width=True)

    elif animo == "Feliz":
        st.write("### ¡Esa es mi hija! Mire este video:")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()

    elif animo == "¡Súper Feliz!":
        st.write("### ¡CELEBRACIÓN TOTAL PARA USTED! 🎉")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.snow()

    st.divider()
    st.link_button("💌 ENVIARLE UN MENSAJE A PAPÁ", "https://wa.me/56992238085")

import streamlit as st
import random

# 1. Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- DISEÑO AVANZADO (CSS) ---
st.markdown("""
    <style>
    /* Imagen de fondo estilo Neón/Retrowave */
    .stApp {
        background-image: url("https://wallpaperaccess.com/full/2641074.gif");
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Capa oscura para que el texto se lea bien */
    .main {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 15px;
    }

    /* Títulos en Neón */
    h1 {
        color: #ff00ff;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
    }

    /* Cuadro de chistes estilo tarjeta tecnológica */
    .stInfo {
        background-color: rgba(20, 20, 20, 0.8);
        border: 1px solid #00ffff;
        color: white;
        border-radius: 10px;
        box-shadow: 0 0 15px #00ffff;
    }

    /* Botón de WhatsApp con logo y color oficial */
    .whatsapp-button {
        background-color: #25D366;
        color: white;
        padding: 12px 24px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LISTADOS (Sus palabras y chistes intactos) ---
palabras = ["Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"]
lista_chistes = ["— En Hawai uno no se hospeda, se aloha.", "— ¿Cómo se llama el campeón japonés de buceo? Tokofondo. ¿Y el segundo? Kasitoko.", "— Ayer pasé por su casa y me tiró una palta… qué palta de respeto.", "— Robinson Crusoe y lo atropellaron.", "— El otro día vi a un otaku triste y lo animé.", "— Ayer metí un libro de récords en la batidora y batí todos los récords.", "— ¿Qué le dice un pan a otro pan? Le presento una miga.", "— Cuando esté triste abraza un zapato. Un zapato consuela.", "— Doctor, doctor, tengo un hueso afuera. ¡Hágalo pasar!", "— Una señora llorando llega a una zapatería: ¿Tiene zapatos de cocodrilo? ¿Qué número calza su cocodrilo?", "— Había una vez un niñito llamado Nintendo, lo atropellaron y dijo: Game Over.", "— Un tipo va al oculista. —Mire la pared. —¿Cuál pared?", "— ¿Cómo se llama su padre? —Igual. —¿Don Igual? —Sí.", "— Un español le pregunta a un inglés: ¿Cómo llaman a los bomberos? —Firemen. —Nosotros por teléfono.", "— ¿Se sabe el chiste del tarro? —No. —¡Qué lata!", "— Había un niñito que se llamaba Tarea. Tarea para la casa. Y Tarea se fue.", "— Tengo un perro que dice “Hola”. —En mi casa tengo un tarro que dice “Nescafé”.", "— ¿Qué le dijo un poste de luz a otro? El último apaga la luz.", "— ¿Aló, está Joaco? —No, Joaco Imprar.", "— Señorita, ¿hayalletas? (Hay galletas)", "— ¿Cómo estornuda un tomate? ¡Ketchup!", "— ¿Qué le dijo un árbol a otro? Nos dejaron plantados.", "— ¿Qué le dijo un techo a otro? Techo de menos.", "— ¿Qué hace una abeja en el gimnasio? Zum-ba.", "— Robinson Crusoe… quedó solo.", "— ¿Cuántos pelos tiene la cola de un caballo? 30.583. ¿Y cómo lo sabe? Esa es otra pregunta."]

if 'chistes_vistos' not in st.session_state or len(st.session_state.chistes_vistos) == len(lista_chistes):
    st.session_state.chistes_vistos = []
chistes_disponibles = [c for c in lista_chistes if c not in st.session_state.chistes_vistos]
chiste_del_momento = random.choice(chistes_disponibles)

if 'saludo' not in st.session_state:
    st.session_state.saludo = random.choice(palabras)

# --- INICIO DE LA APP ---
st.title(f"❤️ ¡Hola, mi Señora {st.session_state.saludo}!")

st.markdown("<p style='text-align: center; color: white;'>Dedicado con todo mi amor para usted, mi reina del universo.</p>", unsafe_allow_html=True)

st.subheader("💬 ¿Cómo se siente usted hoy?")
animo = st.select_slider("", options=["Seleccione", "Triste", "Normal", "Feliz", "¡Súper Feliz!"])

st.divider()

if animo == "Seleccione":
    st.markdown("<h3 style='text-align: center; color: #00ffff;'>✨ Mueva la barrita para comenzar...</h3>", unsafe_allow_html=True)
else:
    if chiste_del_momento not in st.session_state.chistes_vistos:
        st.session_state.chistes_vistos.append(chiste_del_momento)

    if animo == "Triste":
        st.write("### Mi niñita, un chiste fome para alegrar el día:")
        st.info(chiste_del_momento)
        st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg")
    elif animo == "Normal":
        st.write("### ¡Disfrute su día! Aquí uno quizás no tan fome:")
        st.info(chiste_del_momento)
        st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg")
    elif animo == "Feliz":
        st.write("### ¡Esa es mi hija! Mire este video:")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
    elif animo == "¡Súper Feliz!":
        st.write("### ¡CELEBRACIÓN TOTAL! 🎉")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.snow()

    st.write("---")
    # Botón personalizado de WhatsApp con Icono
    st.markdown(f"""
        <div style="text-align: center;">
            <a href="https://wa.me/56992238085" class="whatsapp-button">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="25" height="25">
                ENVIARLE UN MENSAJE A PAPÁ
            </a>
        </div>
    """, unsafe_allow_html=True)

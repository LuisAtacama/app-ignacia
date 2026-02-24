import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- 1. LISTADO DE PALABRAS PARA EL SALUDO ---
palabras = [
    "Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", 
    "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", 
    "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", 
    "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"
]

# --- 2. LISTADO DE CHISTES (TU LISTA DE 26) ---
lista_chistes = [
    "— En Hawai uno no se hospeda, se aloha.",
    "— ¿Cómo se llama el campeón japonés de buceo? Tokofondo. ¿Y el segundo? Kasitoko.",
    "— Ayer pasé por tu casa y me tiraste una palta… qué palta de respeto.",
    "— Robinson Crusoe y lo atropellaron.",
    "— El otro día vi a un otaku triste y lo animé.",
    "— Ayer metí un libro de récords en la batidora y batí todos los récords.",
    "— ¿Qué le dice un pan a otro pan? Te presento una miga.",
    "— Cuando estés triste abraza un zapato. Un zapato consuela.",
    "— Doctor, doctor, tengo un hueso afuera. ¡Hágalo pasar!",
    "— Una señora llorando llega a una zapatería: ¿Tiene zapatos de cocodrilo? ¿Qué número calza su cocodrilo?",
    "— Había una vez un niñito llamado Nintendo, lo atropellaron y dijo: Game Over.",
    "— Un tipo va al oculista. —Mire la pared. —¿Cuál pared?",
    "— ¿Cómo se llama tu padre? —Igual. —¿Don Igual? —Sí.",
    "— Un español le pregunta a un inglés: ¿Cómo llaman a los bomberos? —Firemen. —Nosotros por teléfono.",
    "— ¿Te sabes el chiste del tarro? —No. —¡Qué lata!",
    "— Había un niñito que se llamaba Tarea. Tarea para la casa. Y Tarea se fue.",
    "— Tengo un perro que dice “Hola”. —En mi casa tengo un tarro que dice “Nescafé”.",
    "— ¿Qué le dijo un poste de luz a otro? El último apaga la luz.",
    "— ¿Aló, está Joaco? —No, Joaco Imprar.",
    "— Señor, ¿hayalletas? (Hay galletas)",
    "— ¿Cómo estornuda un tomate? ¡Ketchup!",
    "— ¿Qué le dijo un árbol a otro? Nos dejaron plantados.",
    "— ¿Qué le dijo un techo a otro? Techo de menos.",
    "— ¿Qué hace una abeja en el gimnasio? Zum-ba.",
    "— Robinson Crusoe… quedó solo.",
    "— ¿Cuántos pelos tiene la cola de un caballo? 30.583. ¿Y cómo lo sabes? Esa es otra pregunta."
]

# --- 3. LÓGICA DE MEMORIA (Para no repetir chistes) ---
if 'chistes_vistos' not in st.session_state or len(st.session_state.chistes_vistos) == len(lista_chistes):
    st.session_state.chistes_vistos = []

chistes_disponibles = [c for c in lista_chistes if c not in st.session_state.chistes_vistos]
chiste_del_momento = random.choice(chistes_disponibles)

# Guardamos el saludo para que no cambie cada vez que mueve el slider
if 'saludo' not in st.session_state:
    st.session_state.saludo = random.choice(palabras)

# --- INICIO DE LA APP ---
st.title(f"❤️ ¡Hola, mi Señora {st.session_state.saludo}!")

st.subheader("💬 ¿Cómo te sientes hoy?")
animo = st.select_slider(
    "Mueve la barrita para que papá te responda:",
    options=["Selecciona", "Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

st.write("---")

if animo == "Selecciona":
    st.write("Mueve la barrita de arriba para ver qué tiene papá para ti hoy...")

else:
    # Si elige cualquier estado, le mostramos un chiste y "gastamos" uno de la lista
    if chiste_del_momento not in st.session_state.chistes_vistos:
        st.session_state.chistes_vistos.append(chiste_del_momento)

    if animo == "Triste":
        st.write("### Mi niña, recuerda que siempre te haré sonreír. Mira:")
        st.info(chiste_del_momento)
        st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg")

    elif animo == "Normal":
        st.write("### ¡Disfruta tu día! Aquí va una humorada:")
        st.info(chiste_del_momento)
        st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg")

    elif animo == "Feliz":
        st.write("### ¡Esa es mi hija! Mira este video:")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()

    elif animo == "¡Súper Feliz!":
        st.write("### ¡CELEBRACIÓN TOTAL! 🎉")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.snow()

    st.write("---")
    st.link_button("💌 MANDARLE UN MENSAJE A PAPÁ", "https://wa.me/56992238085")

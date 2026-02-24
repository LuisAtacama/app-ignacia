import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- LISTADO DE PALABRAS PERSONALIZADAS ---
palabras = [
    "Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente", 
    "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria", 
    "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky", 
    "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"
]
palabra_del_dia = random.choice(palabras)

# --- INICIO: SALUDO DINÁMICO ---
st.title(f"❤️ ¡Hola, mi Señora {palabra_del_dia}!")

st.subheader("💬 ¿Cómo se siente hoy?")
animo = st.select_slider(
    "Mueva la barrita, llegará una sorpresa:",
    options=["Selecciona", "Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

st.write("---")

# --- RESPUESTA DINÁMICA ---

if animo == "Selecciona":
    st.write("La amo infinito hijita")

else:
    # 1. Mensajes y contenido según el ánimo
    if animo == "Triste":
        st.write("### Mi niña, recuerda que después de la lluvia siempre sale el sol. Papá siempre está aquí.")
        st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", caption="Un abrazo gigante ❤️")

    elif animo == "Normal":
        st.write("### ¡Qué bueno que tengas un día tranquilo! Disfruta cada minuto.")
        st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg")

    elif animo == "Feliz":
        st.write("### ¡Tu felicidad es mi mayor alegría! Nunca dejes de sonreír.")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()

    elif animo == "¡Súper Feliz!":
        st.write("### ¡ESTO ES FIESTA! Eres la mejor del mundo entero.")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.snow()

    # --- BOTÓN DE WHATSAPP CON TU NÚMERO ---
    st.write("---")
    st.link_button("💌 MANDARLE UN MENSAJE A PAPÁ", "https://wa.me/56992238085")

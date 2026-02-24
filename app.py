import streamlit as st

st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

st.title("❤️ ¡Bienvenida, mi Señora Matemáticas!")

# --- SECCIÓN DE FOTOS ---
st.subheader("📸 Galería de Recuerdos")
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.unsplash.com/photo-1559454403-b8fb88521f11?w=400", caption="Nuestra primera foto")
with col2:
    st.image("https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=400", caption="¡Te amo mucho!")

# --- SECCIÓN DE VIDEO ---
st.subheader("📺 Un video para ti")
# Aquí puedes pegar un link de YouTube de un video que te guste o uno que tú subas
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Reemplaza este link por el que quieras

# --- INTERACCIÓN (FEEDBACK) ---
st.subheader("💬 Hablemos un poquito")
animo = st.select_slider(
    "¿Cómo te sientes hoy, hija?",
    options=["Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

# Aquí la app le responde automáticamente según lo que ella elija
if animo == "Triste":
    st.warning("¡Ánimo, mi niña! Papá está aquí para darte un abrazo gigante. Mira de nuevo la foto de arriba.")
elif animo == "¡Súper Feliz!":
    st.success("¡Esa es mi hija! Tu alegría es la mía. ¡Vamos a celebrar!")
    st.balloons()
else:
    st.info("¡Qué bueno escucharte! Papá siempre está pensando en ti.")

# --- BOTÓN DE RESPUESTA REAL ---
st.write("---")
st.write("Si quieres mandarme un mensaje largo que me llegue al celular:")
st.link_button("💌 ENVIAR MENSAJE A PAPÁ", "https://wa.me/569XXXXXXXX") # Pon tu número de WhatsApp aquí

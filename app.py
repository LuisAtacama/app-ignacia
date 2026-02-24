import streamlit as st

st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

st.title("❤️ ¡Bienvenida, mi Señora Matemáticas!")

# --- SECCIÓN DE FOTOS REALES ---
st.subheader("📸 Nuestros Momentos Especiales")
col1, col2 = st.columns(2)

with col1:
    # Foto 1: Ignacia (la que tiene lentes)
    st.image("https://lh3.googleusercontent.com/d/1xSqdAD-zfwKqtuNmDT4ucUTzPGduc7SI", caption="¡Qué estilo!")

with col2:
    # Foto 2: Ignacia sonriendo
    st.image("https://lh3.googleusercontent.com/d/1MggbWh6rNt6smCp4SSlvCcWzmG5sDLkJ", caption="Tu sonrisa ilumina todo")

# --- INTERACCIÓN ---
st.subheader("💬 Hablemos un poquito")
animo = st.select_slider(
    "¿Cómo te sientes hoy, hija?",
    options=["Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

if animo == "Triste":
    st.warning("¡Ánimo, mi niña! Papá está aquí para darte un abrazo gigante.")
elif animo == "¡Súper Feliz!":
    st.success("¡Esa es mi hija! Tu alegría es la mía.")
    st.balloons()
else:
    st.info("¡Qué bueno escucharte! Papá siempre está pensando en ti.")

st.write("---")
# Cambia el número abajo por el tuyo para que te llegue el WhatsApp
st.link_button("💌 ENVIAR MENSAJE A PAPÁ", "https://wa.me/569XXXXXXXX")

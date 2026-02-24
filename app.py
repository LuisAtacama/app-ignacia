import streamlit as st

# Configuración de la página
st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# Título cariñoso
st.title("❤️ ¡Bienvenida, mi Señora Matemáticas!")

# --- SECCIÓN DE FOTOS REALES (CON TUS LINKS) ---
st.subheader("📸 Nuestros Momentos Especiales")
col1, col2 = st.columns(2)

with col1:
    # Foto: Amor papi hija
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", caption="¡Amor infinito!")

with col2:
    # Foto: Ignacita alegría primer oso
    st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", caption="Tu primer oso y tu gran alegría")

# --- MENSAJE DE PAPÁ ---
st.write("""
### Hijita querida,
Esta es una app que papá hizo especialmente para ti. 
Quiero que sepas lo mucho que te amo y lo orgulloso que estoy de tenerte como hija.
""")

# --- INTERACCIÓN ---
st.subheader("💬 ¿Cómo te sientes hoy?")
animo = st.select_slider(
    "Mueve la barrita aquí abajo:",
    options=["Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

if animo == "Triste":
    st.warning("¡Ánimo, mi niña! Papá está aquí para darte un abrazo gigante. ¡Mira las fotos de arriba para sonreír!")
elif animo == "¡Súper Feliz!":
    st.success("¡Esa es mi hija! Tu alegría es la mía. ¡Vamos a celebrar! 🎈")
    st.balloons()
else:
    st.info("¡Qué bueno escucharte! Papá siempre está pensando en ti. ❤️")

st.write("---")
# RECUERDA: Cambia el número 569XXXXXXXX por tu número real para recibir el WhatsApp
st.link_button("💌 HAZ CLIC AQUÍ PARA ENVIARLE UN MENSAJE A PAPÁ", "https://wa.me/56992238085")

st.caption("Hecho con mucho ❤️ por tu papá.")

import streamlit as st

st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

st.title("❤️ ¡Bienvenida, mi Señora Matemáticas!")

# --- SECCIÓN DE ÁNIMO ---
st.subheader("💬 ¿Cómo te sientes hoy, hija?")
animo = st.select_slider(
    "Mueve la barrita para ver tu sorpresa:",
    options=["Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

st.write("---")

# --- VIDEO ÚNICO DE DRIVE ---
# Este es el nuevo video que me pasaste
st.subheader("📺 Un video especial para ti")
st.video("https://drive.google.com/uc?export=download&id=1wk7a_c_hY1N9eQlrjdBRT1tdbtnxcwtn")

# Reacciones según el ánimo
if animo == "Triste":
    st.info("Hija, aunque estés triste, recuerda que siempre te haré sonreír. ¡Mira el video!")
elif animo == "¡Súper Feliz!":
    st.success("¡Esa alegría es contagiosa! ¡Eres la mejor!")
    st.balloons()
    st.snow()
else:
    st.write("¡Espero que te guste este video que elegí para ti! ❤️")

# --- SECCIÓN DE FOTOS ---
st.write("---")
st.subheader("📸 Nuestros Recuerdos")
col1, col2 = st.columns(2)
with col1:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", caption="¡Amor infinito!")
with col2:
    st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", caption="Tu alegría")

st.write("---")
# RECUERDA: Pon tu número de WhatsApp real aquí (ej: https://wa.me/56912345678)
st.link_button("💌 MANDARLE UN MENSAJE A PAPÁ", "https://wa.me/569XXXXXXXX")

st.caption("Hecho con ❤️ por tu papá.")

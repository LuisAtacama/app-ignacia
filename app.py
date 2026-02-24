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

# --- VIDEO DE YOUTUBE ---
st.subheader("📺 Un mensaje especial de papá")
# He puesto tu video de YouTube aquí:
st.video("https://youtu.be/sB-TdQKWMGI")

# Reacciones según el ánimo
if animo == "Triste":
    st.info("Hija, aunque estés triste, recuerda estas palabras que te dije antes de conocerte. ¡Papá siempre estará para ti!")
elif animo == "¡Súper Feliz!":
    st.success("¡Esa alegría es contagiosa! ¡Eres el mejor regalo de la vida!")
    st.balloons()
    st.snow()
else:
    st.write("¡Este video es de cuando te estábamos esperando con mucha emoción! ❤️")

# --- SECCIÓN DE FOTOS ---
st.write("---")
st.subheader("📸 Nuestros Recuerdos")
col1, col2 = st.columns(2)
with col1:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", caption="¡Amor infinito!")
with col2:
    st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", caption="Tu alegría")

st.write("---")
# RECUERDA: Pon tu número de WhatsApp real aquí
st.link_button("💌 MANDARLE UN MENSAJE A PAPÁ", "https://wa.me/569XXXXXXXX")

st.caption("Hecho con mucho ❤️ por tu papá.")

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

# --- RESPUESTA DINÁMICA CON VIDEOS DE DRIVE ---

if animo == "Triste" or animo == "Normal":
    st.subheader("🐶 ¡Un regalito para que sonrías!")
    st.write("Mira este video que te preparé:")
    # Video del perrito/mascota
    st.video("https://drive.google.com/uc?export=download&id=1CpEGP3sQrKJuPPaX823rf72g9Pyp0PnX")
    st.info("¡Papá siempre está aquí para hacerte reír!")

elif animo == "Feliz" or animo == "¡Súper Feliz!":
    st.subheader("💃 ¡Ese es el ánimo!")
    st.write("¡Me encanta verte así de contenta! Mira:")
    # Video de ella bailando/feliz
    st.video("https://drive.google.com/uc?export=download&id=1FtAyAEg5zW6D8qm46Fh1N-RXOSrJyir_")
    st.balloons()
    if animo == "¡Súper Feliz!":
        st.snow()
        st.success("¡Eres la mejor, Ignacia! Que nada te quite esa sonrisa.")

# --- SECCIÓN DE FOTOS (Las que ya teníamos) ---
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

st.caption("Hecho con ❤️ por tu papá.")

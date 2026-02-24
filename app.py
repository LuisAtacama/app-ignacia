import streamlit as st

st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

st.title("❤️ ¡Bienvenida, mi Señora Matemáticas!")

# --- SECCIÓN DE ÁNIMO (LA LLAVE MAESTRA) ---
st.subheader("💬 ¿Cómo te sientes en este momento?")
animo = st.select_slider(
    "Mueve la barrita para recibir tu sorpresa:",
    options=["Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

st.write("---")

# --- RESPUESTA DINÁMICA ---

if animo == "Triste":
    st.subheader("🧸 Un abrazo para el alma")
    st.write("Hija, cuando estés triste, recuerda que siempre estaré para ti. Mira este video:")
    # Puedes poner un video de YouTube tierno o una canción
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.info("¡Arriba ese ánimo! Eres la niña más fuerte que conozco.")

elif animo == "Normal":
    st.subheader("📸 Un recuerdo para tu día")
    st.write("¡Qué bueno que tengas un día tranquilo! Mira esta foto de nuestro tesoro:")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", caption="¡Tú y yo siempre!")
    st.write("Espero que este recuerdo te saque una sonrisa.")

elif animo == "Feliz":
    st.subheader("🌟 ¡Que nada te detenga!")
    st.write("¡Me encanta que estés feliz! Eres luz pura. Mira lo que tengo para ti:")
    st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", caption="¡Esa alegría es contagiosa!")
    st.balloons() # Lluvia de globos

elif animo == "¡Súper Feliz!":
    st.subheader("🥳 ¡FIESTA TOTAL!")
    st.write("¡ESTO HAY QUE CELEBRARLO! Eres la mejor, mi Señora Matemáticas.")
    # Aquí puedes poner un video de una canción alegre
    st.video("https://www.youtube.com/watch?v=y6120QOlsfU")
    st.balloons() # ¡Muchos globos!
    st.snow()     # ¡Y nieve también para celebrar!

st.write("---")
# No olvides poner tu número real aquí:
st.link_button("💌 CUÉNTAME MÁS POR WHATSAPP", "https://wa.me/569XXXXXXXX")

st.caption("Tu app se actualiza según tu corazón. ❤️")

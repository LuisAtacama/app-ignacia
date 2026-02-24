import streamlit as st
import random

st.set_page_config(page_title="App de Ignacia", page_icon="🎀")

# --- LISTADO DE PALABRAS (Puedes agregar más aquí entre comillas y comas) ---
palabras = ["Matemáticas", "Inteligente", "Preciosa", "Artista", "Científica", "Favorita", "Divertida"]
palabra_del_dia = random.choice(palabras)

# --- INICIO: SOLO TEXTO ---
st.title(f"❤️ ¡Hola, mi Señora {palabra_del_dia}!")

st.subheader("💬 ¿Cómo te sientes en este momento?")
animo = st.select_slider(
    "Mueve la barrita para que papá te responda:",
    options=["Selecciona", "Triste", "Normal", "Feliz", "¡Súper Feliz!"]
)

st.write("---")

# --- RESPUESTA DINÁMICA (Aquí aparece la foto/video solo después de contestar) ---

if animo == "Selecciona":
    st.write("Mueve la barrita de arriba para ver qué tiene papá para ti hoy...")

else:
    # 1. PEQUEÑA FRASE TUYA SEGÚN EL ÁNIMO
    if animo == "Triste":
        st.write("### Mi niña, no olvides que después de la lluvia siempre sale el sol. Aquí estoy para ti.")
        st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", caption="Un abrazo virtual ❤️")

    elif animo == "Normal":
        st.write("### ¡Qué bueno que tengas un día tranquilo! Disfruta cada minuto.")
        st.video("https://youtu.be/sB-TdQKWMGI") # El video de YouTube

    elif animo == "Feliz":
        st.write("### ¡Tu felicidad es mi mayor alegría! Nunca dejes de sonreír.")
        st.image("https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg")
        st.balloons()

    elif animo == "¡Súper Feliz!":
        st.write("### ¡ESTO ES FIESTA! Eres la mejor del mundo entero.")
        st.video("https://youtu.be/sB-TdQKWMGI")
        st.balloons()
        st.snow()

    # --- BOTÓN DE WHATSAPP (Aparece solo después de contestar) ---
    st.write("---")
    st.link_button("💌 MANDARLE UN MENSAJE A PAPÁ", "https://wa.me/569XXXXXXXX")

st.caption("Cada vez que entres, serás una 'Señora' diferente. ❤️")

import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Para mi Ignacia", page_icon="❤️")

# Título con cariño
st.title("❤️ Hola, mi Señora Matemáticas")

# Imagen (Aquí usaremos el link de la foto que ya tienes)
# Nota: Si tienes el link de Google Drive o similar, lo pegamos aquí
st.image("https://images.unsplash.com/photo-1559454403-b8fb88521f11?q=80&w=500", 
         caption="¡Siempre juntos!")

# Tu mensaje tierno
st.write("""
### Hijita querida,
Esta es una app que papá hizo especialmente para ti. 
Quiero que sepas lo mucho que te amo y lo orgulloso que estoy de ti.
""")

# Espacio para que ella te responda
st.subheader("¿Cómo te sientes hoy?")
sentimiento = st.text_input("Escribe aquí tu respuesta...")

if st.button("¡Enviar a Papi!"):
    if sentimiento:
        st.success(f"¡Gracias hija! Ya recibí tu mensaje: '{sentimiento}'")
        st.balloons() # ¡Esto lanza globos en la pantalla!
    else:
        st.warning("Escribe algo antes de enviar.")

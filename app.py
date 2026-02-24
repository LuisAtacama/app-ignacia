import streamlit as st
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- DISEÑO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container { background-color: #FFFFFF; padding: 40px !important; max-width: 600px; }
    h1, h3, p { color: #1A1A1A !important; text-align: center; font-family: 'Inter', sans-serif; }
    .stInfo { 
        background-color: #F8F9FA !important; border-radius: 20px; border: 1px solid #EEE;
        color: #1A1A1A !important; padding: 25px !important; font-size: 19px;
    }
    .whatsapp-btn {
        background-color: #25D366; color: white !important; padding: 14px 28px;
        border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE RESPUESTA ULTRA-VARIADO (ADN LUIS) ---
def responder_como_papi(texto):
    texto = texto.lower()
    
    # 1. Detección de Temas muy específicos para evitar repetición
    # TEMA: SENTIMIENTOS / PENA
    if any(k in texto for k in ["triste", "pena", "llorar", "bajoneada"]):
        return random.choice([
            "¿Pero hijita está bien?, ¿le pasó algo? Pucha más Vivaldi po mi niñita. Le mando un abrazo apretado.",
            "Pucha mi chiquitita, cuénteme bien qué siente para que lo arreglemos. Le mando un abrazo apretado.",
            "Está bien sentirse así a veces, no se guarde nada. Aquí estoy atento. Le mando un abrazo apretado."
        ])

    # TEMA: COLEGIO / TAREAS
    if any(k in texto for k in ["colegio", "tarea", "clase", "profe", "estudiar"]):
        return random.choice([
            "Ya po hijita, estemos Vivaldi con las cosas del colegio. ¿Qué es lo que más le cuesta?",
            "No se abrume con las tareas, vamos por partes. Usted es súper inteligente. Le mando un abrazo apretado.",
            "¡Acuérdese que usted puede con todo! Pucha hay que tener paciencia no más."
        ])

    # TEMA: EL CORAZÓN / ALGUIEN QUE LE GUSTA
    if any(k in texto for k in ["gustar", "alguien", "niño", "niña", "corazon"]):
        return random.choice([
            "Ay mi niñita, los temas del corazón son enredados. Dése tiempo y quiérase mucho usted primero.",
            "Lo más importante es que usted esté feliz. Escuche su corazoncito. Le mando un abrazo apretado.",
            "Pucha, esas cosas a veces confunden, pero usted es inteligente. Tranquila, viva su proceso."
        ])

    # TEMA: CELEBRACIÓN / FOTOS / LOGROS
    if any(k in texto for k in ["gane", "mira", "bien", "foto", "dibujo", "nota", "lindo"]):
        return random.choice([
            "¡AAA QUE BIENNN! Me hace sentir el papá más orgulloso del universo. ¡Se pasó de Vivaldi!",
            "¡Excelente! Qué linda la foto, tiene un gusto increíble. ¡Se pasó!",
            "¡Esa es mi artista! Me encanta lo que hizo. ¡Usted es una campeona!"
        ])

    # TEMA: EXTRAÑAR
    if any(k in texto for k in ["extraño", "papi", "verte"]):
        return random.choice([
            "Yo también la extraño mucho, mi chiquitita linda. Mi corazón está con usted siempre.",
            "Le mando el abrazo más grande del mundo. ¡Pronto nos vemos para hacer algo bacán!",
            "Siempre estoy al ladito suyo en el corazón, no lo olvide nunca."
        ])

    # 2. RESPUESTA DEFAULT (Si no entiende la pregunta, responde algo general pero variado)
    return random.choice([
        "¿Pero qué pasó hijita? Cuénteme más para entenderla bien. La amo mucho siempre.",
        "Pucha mi niñita, cuénteme con confianza. Aquí estoy para lo que necesite.",
        "Ya po, cuénteme el detalle. Hay que estar Vivaldi con todo. Le mando un abrazo apretado."
    ])

# --- 3. BANCO DE FOTOS ---
fotos_galeria = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg", "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg", "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg", "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg", "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg", "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"]

# --- 4. INTERFAZ ---
st.title("❤️ App de Ignacia")

st.write("### 💬 Pregúntele a Papi")
pregunta = st.text_input("Cuénteme algo, mi niñita...", key="chat_input")
if pregunta:
    st.info(f"👨‍👧 **Papi dice:** {responder_como_papi(pregunta)}")

st.divider()

st.write("### 😊 ¿Cómo se siente hoy?")
animo = st.select_slider(label="Estado:", options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"])

if animo != "Seleccione":
    foto = random.choice(fotos_galeria)
    st.image(foto, use_container_width=True)
    st.markdown("<p style='font-style:italic; font-size:18px;'>\"La amo mucho siempre, hijita linda.\"</p>", unsafe_allow_html=True)

st.markdown("""<div style='text-align:center; margin-top:40px;'><a href='https://wa.me/56992238085' class='whatsapp-btn'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='24'> MENSAJE A PAPI</a></div>""", unsafe_allow_html=True)

import streamlit as st
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container { background-color: #FFFFFF; padding: 40px !important; max-width: 600px; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #1A1A1A !important; text-align: center; }
    .frase-papi { text-align: center; font-style: italic; font-size: 19px; color: #1A1A1A; margin-top: 20px; padding: 15px; border-top: 1px solid #EEE; }
    .chiste-box { background-color: #F8F9FA; border-radius: 15px; padding: 25px; text-align: center; font-size: 18px; color: #1A1A1A; margin: 20px 0; border: 1px solid #EEE; line-height: 1.6; white-space: pre-wrap; }
    .whatsapp-btn { background-color: #25D366; color: white !important; padding: 16px 32px; border-radius: 50px; text-decoration: none !important; font-weight: 700; display: inline-flex; align-items: center; gap: 12px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EL BANCO DE RECUERDOS (FOTO + TEXTO EMPAREJADO) ---
galeria_maestra = [
    {"url": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "txt": "Este abrazo me lo guardo en el corazón para siempre. Usted sabe que papi está ahí con usted."},
    {"url": "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "txt": "¡Mire qué carita de felicidad con su oso! Esa alegría suya es lo más importante del mundo."},
    {"url": "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "txt": "¡Aaaaa pero qué estilosa! Me encanta verla así de canchera, tiene un gusto excelente."},
    {"url": "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "txt": "Ahí se ve muy tranquila y valiente. Acuérdese que usted es súper inteligente."},
    {"url": "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "txt": "Pucha que lo pasamos bacán ese día. Me pone muy feliz recordarlo."},
    {"url": "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "txt": "¡Qué buena foto! Se ve muy despierta, así la quiero: ¡Vivaldi siempre!"},
    {"url": "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "txt": "Usted tiene una luz especial. Nunca olvide que no hay nada que cambiar en usted."},
    {"url": "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "txt": "¡Esa es mi artista favorita! Tiene un ojo increíble para capturar momentos."},
    {"url": "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "txt": "Linda mi chiquitita. Aquí estoy atento a lo que necesite siempre."},
    {"url": "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "txt": "¡Aaaaa qué hermosa se ve! Me hace sentir el papá más orgulloso del universo."},
    {"url": "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "txt": "¡Mire qué estilosa! Me encanta esa actitud suya, marcando la diferencia."},
    {"url": "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "txt": "Pucha que se ve linda ahí. Usted tiene una luz que brilla solita."},
    {"url": "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "txt": "Esa mirada me dice que estaba bien Vivaldi en ese momento. ¡Así me gusta!"},
    {"url": "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "txt": "Usted es una niña muy alegre y esa energía se contagia. ¡Aaaa que buena foto!"},
    {"url": "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "txt": "¡Qué buen momento! Me pone muy feliz verla disfrutar las cosas simples."},
    {"url": "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg", "txt": "Usted es súper inteligente y creativa. Nunca deje de inventar cosas nuevas."},
    {"url": "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "txt": "Me encanta esta foto porque sale tal cual es usted. Auténtica y valiente."},
    {"url": "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "txt": "Pucha que lo pasamos bacán. Estos recuerdos son los que más valoro."},
    {"url": "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "txt": "Ahí se ve muy concentrada. Recuerde que con paciencia lo vamos a lograr."},
    {"url": "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "txt": "¡Esa sonrisa lo dice todo! Le mando un abrazo apretado siempre."},
    {"url": "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "txt": "¡Esa es mi chiquitita! Me encanta que sea tan creativa para sus cosas."},
    {"url": "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "txt": "¡Aaaaa pero qué divertida! Me hace reír mucho su ingenio."},
    {"url": "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "txt": "Pucha que se ve bien ahí. Usted tiene un estilo único, hijita linda."},
    {"url": "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg", "txt": "Esa carita me dice que está tramando algo bacán. Confíe en su inteligencia."},
    {"url": "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "txt": "¡Qué buena foto! Me gusta verla así de canchera. Un abrazo apretado."},
    {"url": "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "txt": "Usted es una niña valiente y muy especial. Perfecta tal como es."},
    {"url": "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "txt": "¡Mire qué artista! Tiene un ojo excelente para las fotos. Orgulloso de usted."},
    {"url": "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "txt": "Linda mi niñita. Pucha que lo pasamos bien cuando estamos juntos."},
    {"url": "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "txt": "¡Esa es la actitud! Esté siempre atenta y Vivaldi."},
    {"url": "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "txt": "Usted ilumina todo con esa sonrisa. Gracias por ser así de especial."},
    {"url": "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "txt": "¡Qué lindo lugar! Me encanta que disfrute la naturaleza."},
    {"url": "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "txt": "Pucha que se ve bien ahí. Usted tiene una luz que ilumina todo."},
    {"url": "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "txt": "Ahí la veo muy tranquila. Aquí está papi para apoyarla en todo."},
    {"url": "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg", "txt": "¡Aaaaa pero qué buena foto! Canchera en sus paseos. ¡Vivaldi siempre!"},
    {"url": "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "txt": "Usted es una niña muy habilosa y se nota en todo lo que hace."},
    {"url": "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "txt": "¡Qué linda sonrisa! Nunca deje que nada le quite esa alegría."},
    {"url": "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "txt": "Me encanta este recuerdo. Pucha que lo pasamos bacán ese día."},
    {"url": "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "txt": "Ahí se ve muy valiente. Usted puede con todo lo que se proponga."},
    {"url": "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "txt": "¡Mire qué artista para sacar fotos! Tiene un ojo excelente."},
    {"url": "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg", "txt": "Linda mi niñita. No hay nada que cambiar en usted, es perfecta."},
    {"url": "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "txt": "¡Mire qué estilosa! Tiene un gusto único. ¡Se pasó de Vivaldi!"},
    {"url": "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "txt": "Pucha que se ve linda ahí. Su sonrisa es lo más importante para papi."},
    {"url": "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "txt": "¡Aaaaa pero qué buena foto! Usted es una niña muy especial."},
    {"url": "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "txt": "Ahí se ve muy despierta e inteligente. ¡Siempre Vivaldi, hijita!"},
    {"url": "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "txt": "Me encanta este recuerdo. Pucha que lo pasamos bacán."},
    {"url": "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg", "txt": "Usted tiene un brillo propio, mi chiquitita. Perfecta tal como es."},
    {"url": "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "txt": "¡Qué buena selfie! Me hace reír mucho su ingenio."},
    {"url": "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "txt": "Linda mi niñita. Mi corazón está al ladito suyo siempre."},
    {"url": "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "txt": "¡Esa es mi artista favorita! Siga capturando la vida así de lindo."},
    {"url": "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png", "txt": "Usted es lo mejor que me ha pasado en la vida. ¡La amo mucho!"}
]

# --- 3. SUS CHISTES REALES (LOS QUE SUBIÓ USTED) ---
chistes_reales = [
    "— En Hawai uno no se hospeda, se aloha.",
    "— ¿Cómo se llama el campeón japonés de buceo? \n — Tokofondo. \n — ¿Y el segundo lugar? \n — Kasitoko.",
    "Ayer pasé por tu casa y me tiraste una palta… qué palta de respeto.",
    "Robinson Crusoe y lo atropellaron.",
    "El otro día vi a un otaku triste y lo animé.",
    "Ayer metí un libro de récords en la batidora y batí todos los récords.",
    "— ¿Qué le dice un pan a otro pan? \n — Te presento una miga.",
    "— Cuando estés triste abraza un zapato. \n — Un zapato consuela.",
    "— Doctor, doctor, tengo un hueso afuera. \n — ¡Hágalo pasar!",
    "— ¿Tiene zapatos de cocodrilo? \n — ¿Qué número calza su cocodrilo?",
    "— Había una vez un niñito llamado Nintendo, lo atropellaron y dijo: Game Over.",
    "— ¿Cómo llaman a los bomberos? \n — Firemen. \n — Nosotros los llamamos por teléfono.",
    "— ¿Te sabes el chiste del tarro? \n — No. \n — ¡Qué lata!",
    "— Había un niñito que se llamaba Tarea. \n — Tarea para la casa. \n — Y Tarea se fue.",
    "— Tengo un perro que dice “Hola”. \n — En mi casa tengo un tarro que dice “Nescafé”.",
    "— ¿Qué le dijo un poste de luz a otro? \n — El último apaga la luz.",
    "— ¿Aló, está Joaco? \n — No, Joaco Imprar.",
    "— Señor, ¿hayalletas? (Hay galletas)",
    "— ¿Cómo estornuda un tomate? \n — ¡Ketchup!",
    "— ¿Qué le dijo un árbol a otro árbol? \n — Nos dejaron plantados.",
    "— ¿Qué le dijo un techo a otro techo? \n — Techo de menos.",
    "— ¿Qué hace una abeja en el gimnasio? \n — Zum-ba.",
    "Robinson Crusoe… quedó solo.",
    "— ¿Cuántos pelos tiene la cola de un caballo? \n — 30.583. \n — ¿Y cómo lo sabes? \n — Perdone profesor… pero esa ya es otra pregunta."
]

# --- 4. ESTRUCTURA APP ---
st.title("❤️ Hola, Ignacita linda")

# SECCIÓN RECUERDOS
st.write("### 📸 Un recuerdo para hoy")
animo = st.select_slider(label="¿Cómo se siente?", options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"])

st.divider()

if animo != "Seleccione":
    # Elegimos el objeto completo para que foto y texto COINCIDAN SIEMPRE
    recuerdo = random.choice(galeria_maestra)
    st.image(recuerdo["url"], use_container_width=True)
    st.markdown(f'<p class="frase-papi">"{recuerdo["txt"]}"</p>', unsafe_allow_html=True)
    if animo in ["FELIZ", "MUY FELIZ"]: st.balloons()
else:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

st.divider()

# SECCIÓN CHISTES
st.write("### 🤡 ¡Un chiste para alegrar el día!")
if st.button("¡Cuéntame un chiste, Papi!"):
    chiste_hoy = random.choice(chistes_reales)
    st.markdown(f'<div class="chiste-box">{chiste_hoy}</div>', unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>¡Jajaja! Estemos Vivaldi con la alegría siempre.</p>", unsafe_allow_html=True)

# WhatsApp
st.markdown("""<div style='text-align:center; margin-top:50px;'><a href='https://wa.me/56992238085' class='whatsapp-btn'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='26'> HABLAR CON PAPI</a></div>""", unsafe_allow_html=True)

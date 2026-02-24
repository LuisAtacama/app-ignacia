import streamlit as st
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# --- DISEÑO CSS (PULCRO Y PROFESIONAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container { background-color: #FFFFFF; padding: 40px !important; font-family: 'Inter', sans-serif; max-width: 600px; }
    h1 { color: #1A1A1A !important; font-weight: 700; font-size: 32px; text-align: center; margin-bottom: 10px; }
    h3 { color: #4A4A4A !important; font-weight: 400; font-size: 18px; text-align: center; margin-bottom: 30px; }
    .frase-papi { text-align: center; font-style: italic; font-size: 19px; color: #1A1A1A; margin-top: 20px; padding: 15px; line-height: 1.5; border-top: 1px solid #EEE; }
    .whatsapp-container { text-align: center; margin-top: 50px; }
    .whatsapp-btn { background-color: #25D366; color: white !important; padding: 16px 32px; border-radius: 50px; text-decoration: none !important; font-weight: 700; display: inline-flex; align-items: center; gap: 12px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EL BANCO DE RECUERDOS COMPLETO (50 FOTOS) ---
recuerdos = [
    # BLOQUE 1
    {"url": "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "texto": "Este abrazo me lo guardo en el corazón para siempre. Usted sabe que papi está ahí con usted, pase lo que pase."},
    {"url": "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "texto": "¡Mire qué carita de felicidad con su oso! Esa alegría suya es lo más importante del mundo, mi chiquitita."},
    {"url": "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "texto": "¡Aaaaa pero qué estilosa! Me encanta verla así de canchera, tiene un gusto excelente hijita linda."},
    {"url": "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "texto": "Ahí se ve muy tranquila y valiente. Acuérdese que usted es súper inteligente, no deje que nada la abrume."},
    {"url": "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "texto": "Pucha que lo pasamos bacán ese día. Me pone muy feliz recordarlo, ¡se pasó!"},
    {"url": "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "texto": "¡Qué buena foto! Se ve muy despierta, así la quiero: ¡Vivaldi siempre mi niñita!"},
    {"url": "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "texto": "Usted tiene una luz especial, hijita. Nunca olvide que no hay nada que cambiar en usted, es perfecta así."},
    {"url": "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "texto": "¡Esa es mi artista favorita! Me encanta cómo captura los momentos, tiene un ojo increíble."},
    {"url": "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "texto": "Linda mi chiquitita. Aquí estoy atento a lo que necesite, le mando un abrazo apretado a la distancia."},
    {"url": "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "texto": "¡Aaaaa qué hermosa se ve! Me hace sentir el papá más orgulloso del universo. ¡Se pasó!"},
    # BLOQUE 2
    {"url": "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "texto": "¡Mire qué estilosa! Me encanta esa actitud suya, siempre marcando la diferencia. ¡Se pasó!"},
    {"url": "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "texto": "Pucha que se ve linda ahí. Recuerde siempre que usted tiene una luz que brilla solita, mi niñita."},
    {"url": "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "texto": "Esa mirada me dice que estaba bien Vivaldi en ese momento. ¡Así me gusta verla siempre!"},
    {"url": "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "texto": "Usted es una niña muy alegre y esa energía se contagia. ¡Aaaa que buena foto!"},
    {"url": "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "texto": "¡Qué buen momento! Me pone muy feliz verla disfrutar las cosas simples. La amo mucho siempre."},
    {"url": "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg", "texto": "Usted es súper inteligente y creativa. Nunca deje de inventar cosas nuevas, ¡es una artista!"},
    {"url": "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "texto": "Me encanta esta foto porque sale tal cual es usted. Auténtica y valiente. ¡Se pasó, hijita!"},
    {"url": "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "texto": "Pucha que lo pasamos bacán. Estos recuerdos son los que más valoro de nosotros dos."},
    {"url": "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "texto": "Ahí se ve muy concentrada. Recuerde que si algo le cuesta, hay que tener paciencia, lo vamos a lograr."},
    {"url": "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "texto": "¡Esa sonrisa lo dice todo! Le mando un abrazo apretado para que esa alegría no se le acabe nunca."},
    # BLOQUE 3
    {"url": "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "texto": "¡Esa es mi chiquitita! Me encanta que sea tan creativa para sus cosas. ¡Siga inventando siempre!"},
    {"url": "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "texto": "¡Aaaaa pero qué divertida! Me hace reír mucho su ingenio. Estemos siempre Vivaldi con la alegría."},
    {"url": "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "texto": "Pucha que se ve bien ahí. Usted tiene un estilo único, hijita linda. ¡Se pasó!"},
    {"url": "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg", "texto": "Esa carita me dice que está tramando algo bacán. Confíe siempre en su inteligencia, que es mucha."},
    {"url": "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "texto": "¡Qué buena foto! Me gusta verla así de canchera. Le mando un abrazo apretado desde acá."},
    {"url": "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "texto": "Usted es una niña valiente y muy especial. No hay nada que cambiar en usted, recuérdelo siempre."},
    {"url": "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "texto": "¡Mire qué artista! Tiene un ojo excelente para las fotos. Me hace sentir muy orgulloso."},
    {"url": "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "texto": "Linda mi niñita. Pucha que lo pasamos bien cuando estamos juntos. La extraño mucho siempre."},
    {"url": "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "texto": "¡Esa es la actitud! Esté siempre atenta y Vivaldi, pero sin perder esa ternura suya."},
    {"url": "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "texto": "Usted ilumina todo con esa sonrisa. Gracias por ser así de especial conmigo, mi chiquitita."},
    # BLOQUE 4
    {"url": "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "texto": "¡Qué lindo lugar! Me encanta que disfrute la naturaleza. Esté siempre atenta a las cosas bellas de la vida."},
    {"url": "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "texto": "Pucha que se ve bien ahí. Usted tiene una luz que ilumina todo el paisaje. ¡Se pasó!"},
    {"url": "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "texto": "Ahí la veo muy tranquila. Recuerde que cuando necesite paz, aquí está papi para apoyarla en todo."},
    {"url": "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg", "texto": "¡Aaaaa pero qué buena foto! Me gusta verla así de canchera en sus paseos. ¡Vivaldi siempre!"},
    {"url": "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "texto": "Usted es una niña muy habilosa y se nota en todo lo que hace. ¡Me hace sentir muy orgulloso!"},
    {"url": "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "texto": "¡Qué linda sonrisa! Nunca deje que nada le quite esa alegría, mi chiquitita linda."},
    {"url": "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "texto": "Me encanta este recuerdo. Pucha que lo pasamos bacán ese día, ¿cierto? Le mando un abrazo apretado."},
    {"url": "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "texto": "Ahí se ve muy valiente. Acuérdese que usted puede con todo lo que se proponga, hijita inteligente."},
    {"url": "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "texto": "¡Mire qué artista para sacar fotos! Tiene un ojo excelente. ¡Siga capturando momentos así!"},
    {"url": "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg", "texto": "Linda mi niñita. No hay nada que cambiar en usted, es perfecta tal como es. La amo mucho siempre."},
    # BLOQUE 5
    {"url": "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "texto": "¡Mire qué estilosa mi niñita! Me encanta cómo combina todo, tiene un gusto único. ¡Se pasó de Vivaldi!"},
    {"url": "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "texto": "Pucha que se ve linda ahí. Nunca olvide que su sonrisa es lo más importante para papi, ¿ya?"},
    {"url": "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "texto": "¡Aaaaa pero qué buena foto! Me gusta verla así de canchera. Usted es una niña muy especial y valiente."},
    {"url": "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "texto": "Ahí se ve muy despierta e inteligente. Así la quiero: ¡siempre Vivaldi con sus cosas, hijita linda!"},
    {"url": "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "texto": "Me encanta este recuerdo. Pucha que lo pasamos bacán. Le mando un abrazo apretado desde acá."},
    {"url": "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg", "texto": "Usted tiene un brillo propio, mi chiquitita. No hay nada que cambiar en usted, es perfecta tal como es."},
    {"url": "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "texto": "¡Qué buena selfie! Me hace reír mucho su ingenio. Gracias por compartir estos momentos conmigo."},
    {"url": "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "texto": "Linda mi niñita. Recuerde que aunque estemos a distancia, mi corazón está al ladito suyo siempre."},
    {"url": "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "texto": "¡Esa es mi artista favorita! Siga capturando la vida así de lindo. ¡Me hace sentir muy orgulloso!"},
    {"url": "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png", "texto": "Usted es lo mejor que me ha pasado en la vida. ¡Acuérdese siempre que la amo mucho!"}
]

# --- 3. ESTRUCTURA DE LA APP ---
st.title("❤️ Hola, Ignacita linda")
st.write("### ¿Cómo se siente usted hoy?")

# Selector de ánimo
animo = st.select_slider(
    label="",
    options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"]
)

st.divider()

if animo != "Seleccione":
    # Elige un recuerdo aleatorio de la lista de 50
    recuerdo_hoy = random.choice(recuerdos)
    st.image(recuerdo_hoy["url"], use_container_width=True)
    
    # Muestra el texto que calza con esa foto
    st.markdown(f'<p class="frase-papi">"{recuerdo_hoy["texto"]}"</p>', unsafe_allow_html=True)
    
    # Animaciones especiales
    if animo in ["FELIZ", "MUY FELIZ"]:
        st.balloons()
else:
    # Pantalla de bienvenida
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    st.markdown('<p class="frase-papi">Mueva la barra de arriba para ver algo que le preparé con mucho cariño...</p>', unsafe_allow_html=True)

# --- 4. ACCESO DIRECTO A PAPI ---
st.markdown(f"""
    <div class="whatsapp-container">
        <a href="https://wa.me/56992238085" class="whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="26">
            HABLAR CON PAPI
        </a>
    </div>
""", unsafe_allow_html=True)

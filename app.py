import streamlit as st
import random
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN E INVENTARIO (SEGÚN SUS ARCHIVOS)
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# Listado oficial de "Señoras" [cite: 17]
SENORAS = ["Loquita", "Molita", "Dinosauria", "Cuadernita", "Matemáticas", "de la Lota", "Monopoly", "Pepinosky", "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"]

# Chistes con saltos de línea y sin citaciones técnicas 
CHISTES = [
    "— En Hawai uno no se hospeda,\n— se aloha.",
    "— ¿Cómo se llama el campeón japonés de buceo?\n— Tokofondo.\n— ¿Y el segundo lugar?\n— Kasitoko.",
    "— ¿Qué le dice un pan a otro pan?\n— Te presento una miga.",
    "— Tengo un perro que dice 'Hola'.\n— En mi casa tengo un tarro que dice 'Nescafé'.",
    "— ¿Qué hace una abeja en el gimnasio?\n— Zum-ba.",
    "— ¿Qué le dijo un techo a otro techo?\n— Techo de menos.",
    "— ¿Te sabes el chiste del tarro?\n— No.\n— ¡Qué lata!",
    "— Había una vez un niñito llamado Nintendo, lo atropellaron y dijo:\n— Game Over."
]

# Fotos de su lista (se mantiene la lógica aleatoria)
FOTOS_RANDOM = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg", "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg", "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg", "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg", "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg", "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"]

VIDEOS_RANDOM = ["https://youtu.be/sB-TdQKWMGI", "https://youtu.be/IBExxlSBbdE", "https://youtu.be/4Bt2LytMb-o", "https://youtu.be/SLhpt5vxQIw", "https://youtu.be/6Qz637nhLKc", "https://youtu.be/zBN-6NEGyzM", "https://youtu.be/leAF95qMGCg", "https://youtu.be/Rgl4n3jWGCQ"]

# ==========================================
# 2. IA: ADN LUIS v9.0 (CONTEXTO INTEGRAL) [cite: 17-56]
# ==========================================
def generar_respuesta_papi(mensaje_usuario, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        # Aquí volcamos TODO el contenido de su archivo Word
        prompt_sistema = """
        Eres Luis, el papá de Ignacia Albornoz Osses ("Ignacita"). Tu tono es tierno, protector y cercano[cite: 19, 24].
        REGLAS DE ORO:
        - Habla SIEMPRE de USTED. Nunca tutees.
        - Eres chileno: usa un lenguaje natural, cálido y breve.
        
        NÚCLEO FAMILIAR:
        - Aída Osses Herrera: Es la mamá. Se llevan muy bien, con respeto y afecto. Son un equipo para cuidarla[cite: 23, 27, 29, 54].
        - Tío Tomás Ignacio: Tu hermano cercano en Barcelona, de la empresa 'Gudslip'[cite: 34, 35].
        - Tatis Taimes y Abuelita Marta: Tus padres (abuelos fallecidos) que la adoraban profundamente[cite: 36, 37].
        - Tío Claudio: Tu hermano en La Serena (neutralidad)[cite: 32, 53].
        
        FAMILIA MATERNA:
        - Nona (Aída) y Tata Ignacio: Abuelos maternos muy cariñosos[cite: 39, 40].
        - Tío Nacho, Tía Ale, y los primos adolescentes Lautaro y Aynara[cite: 41, 42, 43].
        
        AMISTADES:
        - Sofía y Paz: Vecinas de la infancia ("niñas de la casa 6")[cite: 45].
        - Tío Jean Paul Olhaberry: Ilusionista y gran amigo tuyo[cite: 48].
        - Sergio Aldunate: Gran amigo de siempre[cite: 49].
        - Yoly: Amiga de Aída en Santiago[cite: 46].

        SI PREGUNTA POR QUÉ NO VIVEN JUNTOS:
        - "A veces los papás no son pareja, pero siempre somos un equipo para cuidarte"[cite: 55].
        """
        
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-6:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})
        
        response = client.chat.completions.create(model="gpt-4o-mini", messages=mensajes, temperature=0.7)
        return response.choices[0].message.content
    except:
        return "Pucha mi amorcito, la señal anda malita, pero aquí está su pAAPi."

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN Y PORTADA
# ==========================================
if "acceso" in st.query_params or st.session_state.get("autenticado"):
    st.session_state.pagina = 'principal'
    st.session_state.autenticado = True
else:
    st.session_state.pagina = 'inicio'

if st.session_state.pagina == 'inicio':
    st.markdown("""<style>
        [data-testid="stAppViewContainer"] { background-color: black !important; }
        .portada-wrapper {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: black; display: flex; align-items: center; justify-content: center;
            z-index: 999; overflow: hidden;
        }
        .container-central { position: relative; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; }
        .video-gif { max-width: 100%; max-height: 100%; object-fit: contain; }
        .logo-sobre { position: absolute; width: 60%; max-width: 400px; z-index: 1000; animation: emerger 2.5s ease-out forwards; }
        @keyframes emerger { 0% { opacity: 0; transform: scale(0.6); } 100% { opacity: 1; transform: scale(1); } }
        .stButton button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; opacity: 0; z-index: 1001; cursor: pointer; }
    </style>""", unsafe_allow_html=True)

    if st.button("ENTRAR"):
        st.query_params["acceso"] = "vivaldi"
        st.session_state.autenticado = True
        st.session_state.senora = random.choice(SENORAS)
        st.session_state.contenido = random.choice([{"tipo": "foto", "url": f} for f in FOTOS_RANDOM] + [{"tipo": "video", "url": v} for v in VIDEOS_RANDOM])
        st.rerun()

    st.markdown(f'<div class="portada-wrapper"><div class="container-central"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" class="video-gif"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre"></div></div>', unsafe_allow_html=True)

else:
    st.markdown("""<style> [data-testid="stAppViewContainer"] { background-color: white !important; } </style>""", unsafe_allow_html=True)
    
    if 'senora' not in st.session_state: st.session_state.senora = random.choice(SENORAS)
    if 'contenido' not in st.session_state: st.session_state.contenido = {"tipo": "foto", "url": FOTOS_RANDOM[0]}

    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.senora}!")
    st.subheader("¿Cómo está usted?")
    
    if st.session_state.contenido["tipo"] == "foto":
        st.image(st.session_state.contenido["url"], use_container_width=True)
    else:
        st.video(st.session_state.contenido["url"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 14px; border-radius: 50px; text-decoration: none; font-weight: bold; width: 100%; max-width: 300px; text-align: center; display: block; margin: 0 auto;'>📲 HABLAR CON PAPI REAL</a>""", unsafe_allow_html=True)
    st.divider()
    
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.info(random.choice(CHISTES))

    st.write("### 💬 Chat con pAAPi")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("Escriba aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        respuesta = generar_respuesta_papi(prompt, st.session_state.messages)
        with st.chat_message("assistant"): st.write(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

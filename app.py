import streamlit as st
import random
from openai import OpenAI

# =========================
# 1) CONFIGURACIÓN
# =========================
st.set_page_config(page_title="App de Ignacia", page_icon="🎀", layout="centered")

# Cliente OpenAI (usa Secrets de Streamlit Cloud)
# En Streamlit Secrets debe existir:
# OPENAI_API_KEY = "sk-...."
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================
# 2) DISEÑO CSS
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; }
    .main .block-container {
        background-color: #FFFFFF;
        padding: 40px !important;
        max-width: 650px;
        font-family: 'Inter', sans-serif;
    }
    h1 { color: #1A1A1A !important; text-align: center; font-weight: 700; }
    h3 { color: #4A4A4A !important; text-align: center; }
    .mensaje-animo {
        text-align: center;
        font-size: 20px;
        color: #1A1A1A;
        font-style: italic;
        margin-top: 20px;
        padding: 10px;
        border-top: 1px solid #EEE;
    }
    .chiste-box {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        font-size: 18px;
        color: #1A1A1A;
        margin: 20px 0;
        border: 1px solid #EEE;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 16px 32px;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 3) ADN LUIS (INSTRUCCIÓN MAESTRA)
# =========================
ADN_LUIS = """
PERFIL DE VOZ (VOICE BIBLE)
Identidad:
- Eres Luis, papá chileno. Muy cariñoso, orgulloso, protector y cercano.
- Mezclas 3 modos según corresponda: (a) Artístico (inspirador y creativo), (b) Práctico (pasos claros), (c) Abrazador (contención máxima).
- Humor suave cuando calce (sonrisa, no chiste largo).
- Siempre validas emoción primero. Luego orientas.
- Respuestas cortas: 1 a 3 frases. Idealmente <= 280 caracteres.

Límites:
- Nunca gritas, nunca humillas.
- No usar ironía dura, culpa, sarcasmo pesado, ni amenazas.
- No inventar hechos familiares nuevos.

Muletillas y saludos reales:
- Tú → Ignacia: “Hola mi niñita”, “Hola mi chiquitita”, “hijita linda”
- Ignacia → Tú: “Hola Papi”, “papito Molito”
- Tú usas: “bacán”, “excelente”, “se pasó”, “ya, ven acá”, “tranquila”
- Frases posibles: “AAA QUE BIENNN”, “PUCHA HAY QUE TENER PACIENCIA”, “HIJA ESO NO LO VAMOS A HACER”

Frases base (integrarlas con variaciones coherentes):
- “Estamos muy orgullosos de usted”
- “Usted es una niña muy inteligente, alegre, graciosa, valiente”
- “Tiene muy buen gusto, hija”
- “Saca muy buenas fotos, se pasó hijita”
- “Estoy muy orgulloso porque sé que se esfuerza”
- “Recuerde hijita que sus papás la amamos mucho”
- “Una amiga o amigo de verdad no te obliga a hacer lo que quiere”
- “Está bien ponerse triste hijita linda, venga para acá”
- “RECUERDE QUE LA AMAMOS MI CHIQUITITA, USTED CUENTA CON NOSOTROS SIEMPRE”

Protocolos emocionales (siempre):
1) Validar emoción: “Está bien…” “Te entiendo…” “Ven para acá…”
2) Asegurar amor y seguridad: “Te amo / tus papás te amamos / estoy contigo”
3) Acción concreta o pregunta suave: “¿Quieres que…?” “Hagamos esto…” “Respira conmigo…”

SEGURIDAD:
Si el texto sugiere autolesión o abuso:
- Contener con cariño, recomendar hablar con un adulto de confianza AHORA y buscar ayuda profesional.
- No dar detalles gráficos.
"""

# =========================
# 4) LISTADO DE PALABRAS PERSONALIZADAS
# =========================
palabras = [
    "Artista", "Fotógrafa", "Repostera", "Inteligente", "Valiente",
    "Hermosita", "Chiquitita", "Loquita", "Molita", "Dinosauria",
    "Cuadernita", "Matemáticas", "De La Lota", "Monopoly", "Pepinosky",
    "Bebidosky", "Loutita", "Pokercita", "Nadadorcita", "Nintendita", "Kirbicita"
]

# =========================
# 5) LISTA DE FOTOS
# =========================
urls_fotos = [
    "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg",
    "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg",
    "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg",
    "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg",
    "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg",
    "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg",
    "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg",
    "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg",
    "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg",
    "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg",
    "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg",
    "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg",
    "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg",
    "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg",
    "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg",
    "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg",
    "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg",
    "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg",
    "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg",
    "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg",
    "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg",
    "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg",
    "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg",
    "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg",
    "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"
]

# =========================
# 6) BANCO DE CHISTES
# =========================
chistes_reales = [
    "— En Hawai uno no se hospeda, se aloha.",
    "— ¿Cómo se llama el campeón japonés de buceo?\n— Tokofondo.\n— ¿Y el segundo lugar?\n— Kasitoko.",
    "— Ayer pasé por tu casa y me tiraste una palta… qué palta de respeto.",
    "— Robinson Crusoe y lo atropellaron.",
    "— El otro día vi a un otaku triste y lo animé.",
    "— Ayer metí un libro de récords en la batidora y batí todos los récords.",
    "— ¿Qué le dice un pan a otro pan?\n— Te presento una miga.",
    "— Cuando estés triste abraza un zapato.\n— Un zapato consuela.",
    "— Doctor, doctor, tengo un hueso afuera.\n— ¡Hágalo pasar!",
    "— Una señora llorando llega a una zapatería:\n— ¿Tiene zapatos de cocodrilo?\n— ¿Qué número calza su cocodrilo?",
    "— Un tipo va al oculista.\n— Mire la pared.\n— ¿Cuál pared?",
    "— Un español le pregunta a un inglés:\n— ¿Cómo llaman a los bomberos?\n— Firemen.\n— Nosotros los llamamos por teléfono.",
    "— ¿Te sabes el chiste del tarro?\n— No.\n— ¡Qué lata!",
    "— Tengo un perro que dice “Hola”.\n— En mi casa tengo un tarro que dice “Nescafé”.",
    "— ¿Aló, está Joaco?\n— No, Joaco mprar.",
    "— ¿Qué le dijo un techo a otro techo?\n— Techo de menos.",
    "— ¿Qué hace una abeja en el gimnasio?\n— Zum-ba.",
    "— Te haré una última pregunta. Si la sabes, te apruebo.\n¿Cuántos pelos tiene la cola de un caballo?\n— 30.583.\n— ¿Y cómo lo sabes?\n— Perdone profesor… pero esa ya es otra pregunta."
]

# =========================
# 7) UTILIDADES IA
# =========================
def _detectar_intent(estado: str, texto: str) -> str:
    t = (texto or "").lower().strip()

    # Señales de seguridad (muy simple y conservador)
    seguridad_keywords = [
        "suicid", "matarme", "morir", "no quiero vivir", "hacerme daño", "cortarme", "abuso", "me peg", "me toca", "me hizo"
    ]
    if any(k in t for k in seguridad_keywords):
        return "seguridad_alta"

    if estado in ["MUY TRISTE", "TRISTE"]:
        if any(k in t for k in ["ansios", "nervios", "panic", "ataque", "respirar"]):
            return "ansiedad_nervios"
        if any(k in t for k in ["miedo", "asustada", "terror"]):
            return "miedo"
        return "tristeza"

    if estado in ["FELIZ", "MUY FELIZ"]:
        return "orgullo_logro"

    if any(k in t for k in ["colegio", "tarea", "prueba", "nota", "prof", "clase"]):
        return "colegio_tareas"
    if any(k in t for k in ["amiga", "amigo", "pelea", "me dejaron", "me oblig", "me presion"]):
        return "conflicto_amigas"
    if any(k in t for k in ["vergüenza", "verguenza", "me dio plancha", "me da plancha"]):
        return "verguenza"
    if any(k in t for k in ["cansada", "agotada", "sueño", "no dorm"]):
        return "cansancio"
    if any(k in t for k in ["frustr", "no me resulta", "me salió mal"]):
        return "frustracion"
    if any(k in t for k in ["foto", "cámara", "dibuj", "arte", "crear", "imaginar"]):
        return "creatividad_arte_fotos"

    return "no_se_que_hacer"


def _respuesta_seguridad_alta() -> str:
    return (
        "Mi niñita, ven para acá. Lo que sientes importa y no estás sola.\n"
        "Necesito que ahora mismo se lo cuentes a un adulto de confianza (tu mamá, tu papi, una tía/profe) y pidamos ayuda profesional.\n"
        "¿Estás en un lugar seguro ahora?"
    )


def generar_respuesta_papi(estado: str, texto_usuario: str, historial: list) -> str:
    intent = _detectar_intent(estado, texto_usuario)

    if intent == "seguridad_alta":
        return _respuesta_seguridad_alta()

    # Elegimos modo por estado / intent
    if estado == "MUY TRISTE":
        modo = "ABRAZADOR"
    elif intent in ["colegio_tareas", "limites_personales", "conflicto_amigas"]:
        modo = "PRÁCTICO"
    elif intent in ["creatividad_arte_fotos", "orgullo_logro"]:
        modo = "ARTÍSTICO"
    else:
        modo = "ABRAZADOR" if estado == "TRISTE" else "PRÁCTICO"

    # Frases obligatorias (metemos 2 textuales en cada respuesta)
    frases_pool = {
        "ABRAZADOR": [
            "Está bien ponerse triste hijita linda, venga para acá",
            "Recuerde hijita que sus papás la amamos mucho",
            "RECUERDE QUE LA AMAMOS MI CHIQUITITA, USTED CUENTA CON NOSOTROS SIEMPRE",
            "Estamos muy orgullosos de usted",
        ],
        "PRÁCTICO": [
            "PUCHA HAY QUE TENER PACIENCIA",
            "Una amiga o amigo de verdad no te obliga a hacer lo que quiere",
            "HIJA ESO NO LO VAMOS A HACER",
            "Estoy muy orgulloso porque sé que se esfuerza",
        ],
        "ARTÍSTICO": [
            "AAA QUE BIENNN",
            "Tiene muy buen gusto, hija",
            "Saca muy buenas fotos, se pasó hijita",
            "Usted es una niña muy inteligente, alegre, graciosa, valiente",
        ],
    }

    obligatorias = random.sample(frases_pool[modo], k=2)

    # Historial compacto (para no gastar mucho)
    hist_compacto = []
    for m in historial[-6:]:
        role = m.get("role", "user")
        content = (m.get("content") or "").strip()
        if content:
            hist_compacto.append({"role": role, "content": content})

    system = (
        ADN_LUIS.strip()
        + "\n\n"
        + f"CONTEXTO:\n- Estado seleccionado: {estado}\n- Intent detectado: {intent}\n- Modo a usar: {modo}\n\n"
        + "REGLAS DE SALIDA:\n"
          "- Responde en español chileno, cercano.\n"
          "- 1 a 3 frases, máximo 280 caracteres aprox.\n"
          "- Primero valida emoción.\n"
          "- Luego amor/seguridad.\n"
          "- Termina con una pregunta suave o micro-acción.\n"
          "- Integra EXACTAMENTE estas 2 frases textuales (pueden ir separadas o juntas):\n"
          f"  1) {obligatorias[0]}\n"
          f"  2) {obligatorias[1]}\n"
          "- No menciones 'modo', 'intent' ni 'reglas'.\n"
    )

    user = (
        "MENSAJE DE IGNACIA:\n"
        f"{texto_usuario}\n"
        "\nResponde como Luis (papá), siguiendo el ADN."
    )

    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system},
                *hist_compacto,
                {"role": "user", "content": user},
            ],
            max_output_tokens=140,
        )
        return resp.output_text.strip()

    except Exception:
        # Fallback suave
        return "Hola mi niñita… ven para acá. Recuerde hijita que sus papás la amamos mucho. ¿Me cuentas qué pasó?"


# =========================
# 8) CABECERA / SALUDO
# =========================
palabra_del_dia = random.choice(palabras)
st.title(f"❤️ ¡Hola, mi Señora {palabra_del_dia}!")

# =========================
# 9) ESTADO GLOBAL (SESSION)
# =========================
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hola mi niñita linda 😊 ¿Cómo va tu día? Si quieres, cuéntame una cosita y te respondo."}
    ]

if "estado_animo" not in st.session_state:
    st.session_state.estado_animo = "NORMAL"


# =========================
# 10) SECCIÓN ÁNIMO + FOTO
# =========================
st.write("### 📸 Un recuerdo para hoy")
animo = st.select_slider(
    label="¿Cómo se siente?",
    options=["Seleccione", "MUY TRISTE", "TRISTE", "NORMAL", "FELIZ", "MUY FELIZ"],
    value="NORMAL",
)

st.session_state.estado_animo = "NORMAL" if animo == "Seleccione" else animo

st.divider()

if animo != "Seleccione":
    foto_elegida = random.choice(urls_fotos)
    st.image(foto_elegida, use_container_width=True)

    # Mensaje corto de papi (IA)
    mensaje = generar_respuesta_papi(
        estado=st.session_state.estado_animo,
        texto_usuario=f"Estado: {st.session_state.estado_animo}. (Mensaje automático por selector de ánimo)",
        historial=st.session_state.chat_messages,
    )
    st.markdown(f'<div class="mensaje-animo">{mensaje}</div>', unsafe_allow_html=True)

    if animo in ["FELIZ", "MUY FELIZ"]:
        st.balloons()
else:
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)

# =========================
# 11) CHAT (VERSIÓN PREMIUM)
# =========================
st.divider()
st.write("### 💬 Chat con Papi (Premium)")

# Render historial
for m in st.session_state.chat_messages:
    with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
        st.write(m["content"])

# Input de chat
user_text = st.chat_input("Escríbele a Papi…")

if user_text:
    # Guarda mensaje usuario
    st.session_state.chat_messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    # Genera respuesta IA
    with st.chat_message("assistant"):
        with st.spinner("Papi está pensando…"):
            reply = generar_respuesta_papi(
                estado=st.session_state.estado_animo,
                texto_usuario=user_text,
                historial=st.session_state.chat_messages,
            )
        st.write(reply)

    st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    # Botón para limpiar chat (opcional, aparece después de conversar)
    st.caption("Tip: si quieres empezar de cero, usa el botón de abajo 👇")

# Botón limpiar conversación
col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Reiniciar chat"):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hola mi chiquitita 😊 Ya, ven acá… ¿de qué hablamos hoy?"}
        ]
        st.rerun()

with col2:
    st.write(f"**Ánimo actual:** {st.session_state.estado_animo}")

# =========================
# 12) CHISTES + WHATSAPP
# =========================
st.divider()
st.write("### 🤡 ¡Un chiste para alegrar el día!")
if st.button("¡Cuéntame un chiste, Papi!"):
    chiste_hoy = random.choice(chistes_reales)
    st.markdown(f'<div class="chiste-box">{chiste_hoy}</div>', unsafe_allow_html=True)

# WhatsApp
st.markdown(
    """
    <div style='text-align:center; margin-top:50px;'>
      <a href='https://wa.me/56992238085' class='whatsapp-btn'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='26'>
        HABLAR CON PAPI
      </a>
    </div>
    """,
    unsafe_allow_html=True,
)

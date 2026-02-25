import streamlit as st
import random
from openai import OpenAI
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# CSS para portada negra total y entrada táctil
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .portada-negra {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: black; display: flex; align-items: center; justify-content: center; z-index: 999;
    }
    .logo-sobre { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
    
    /* El botón invisible que cubre toda la pantalla */
    .stButton > button {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 9999; cursor: pointer;
    }
    
    /* Estilo para los botones internos de la app */
    .boton-interno button {
        position: relative !important; width: 100% !important; height: auto !important;
        background-color: #f0f2f6 !important; color: black !important; opacity: 1 !important;
        z-index: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTOR DE CARGA ROBUSTO (CSV DIRECTO)
# ==========================================
def cargar_datos_viva_voz():
    senoras, chistes, adn, error = [], [], "", None
    try:
        # Extraemos el link de los Secrets
        base_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        # Limpiamos el link para el formato de exportación directa
        base_url = base_url.split('/edit')[0]
        if not base_url.endswith("/"): base_url += "/"
        
        # URLs para descarga directa (evita el Error 400 de la librería estándar)
        url_s = f"{base_url}export?format=csv&sheet=Senoras"
        url_ch = f"{base_url}export?format=csv&sheet=Chistes"
        url_adn = f"{base_url}export?format=csv&sheet=Contexto"

        # Carga de datos con Pandas
        df_s = pd.read_csv(url_s)
        senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()

        df_ch = pd.read_csv(url_ch)
        chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()

        df_adn = pd.read_csv(url_adn)
        adn = "\\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())

    except Exception as e:
        error = str(e)
    
    # Valores de emergencia por si falla el Drive
    if not senoras:
        senoras = ["Señora (Sin Conexión)"]
        chistes = ["Pucha, no pude cargar los chistes del Drive."]
        adn = "Eres Luis, el papá de Ignacita. Habla de USTED."
    
    return senoras, chistes, adn, error

# Inicializar datos en la sesión para que no se pierdan al refrescar
if "DATOS" not in st.session_state:
    s, ch, adn, err = cargar_datos_viva_voz()
    st.session_state.DATOS = {"s": s, "ch": ch, "adn": adn, "err": err}

# Fotos de la galería
FOTOS = [
    "https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", 
    "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg",
    "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg",
    "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg"
]

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    # --- PANTALLA DE PORTADA ---
    st.markdown(f'''
        <div class="portada-negra">
            <img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%">
            <img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre">
        </div>
    ''', unsafe_allow_html=True)
    
    # El botón invisible que permite entrar tocando cualquier parte
    if st.button("ENTRAR", key="entrar_app"):
        st.session_state.autenticado = True
        st.session_state.senora_actual = random.choice(st.session_state.DATOS["s"])
        st.session_state.foto_actual = random.choice(FOTOS)
        st.rerun()

else:
    # --- INTERIOR DE LA APP ---
    
    # Aviso si hubo problemas con el Drive
    if st.session_state.DATOS["err"]:
        st.warning(f"Aviso de conexión: {st.session_state.DATOS['err']}")

    st.title(f"❤️ ¡Hola, mi {st.session_state.senora_actual}!")
    st.image(st.session_state.foto_actual, use_container_width=True)
    
    # Botón de WhatsApp
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; margin-bottom: 20px;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)

    # Botón de Chistes
    st.markdown('<div class="boton-interno">', unsafe_allow_html=True)
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="btn_chiste"):
        st.info(random.choice(st.session_state.DATOS["ch"]))
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.write("### 💬 Chat con pAAPi")

    # Historial de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Entrada de texto del chat
    if p := st.chat_input("¿Qué me quiere decir, mi amor?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": st.session_state.DATOS["adn"]}] + st.session_state.messages
            )
            r = res.choices[0].message.content
        except Exception:
            r = "Pucha mi amorcito, la señal está fallando pero pAAPi te adora."

        with st.chat_message("assistant"):
            st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})

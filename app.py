import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN Y CONEXIÓN
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# Intentamos conectar con el Excel usando la llave de los Secrets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error crítico de conexión: {e}")
    conn = None

# ==========================================
# 2. MOTOR DE CARGA (EL CEREBRO)
# ==========================================
def cargar_datos_maestros():
    # Valores de respaldo (por si el Excel falla)
    senoras = ["Loquita", "Molita"]
    chistes = ["— ¿Qué le dice un pan a otro pan? — Te presento una miga."]
    adn_pasado = "Eres Luis, el papá de Ignacita. Habla de USTED. Eres tierno y protector."
    aprendizajes_recientes = ""

    if conn:
        try:
            # Forzamos lectura fresca (ttl=0)
            df_s = conn.read(worksheet="Senoras", ttl=0)
            if not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().tolist()
            
            df_ch = conn.read(worksheet="Chistes", ttl=0)
            if not df_ch.empty:
                chistes = df_ch.iloc[:, 0].dropna().tolist()
            
            df_adn = conn.read(worksheet="Contexto", ttl=0)
            if not df_adn.empty:
                adn_pasado = "\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
            
            df_ap = conn.read(worksheet="Aprendizajes", ttl=0)
            if not df_ap.empty:
                lista_ap = []
                for _, fila in df_ap.iterrows():
                    if pd.notna(fila.get('Fecha')) and pd.notna(fila.get('Detalle')):
                        lista_ap.append(f"{fila['Fecha']}: {fila['Detalle']}")
                aprendizajes_recientes = "\n".join(lista_ap)
        except Exception as e:
            st.warning(f"Aviso: Cargando modo local. Error Excel: {e}")
            
    return senoras, chistes, adn_pasado, aprendizajes_recientes

# Inicializar los datos en la memoria de la app
if "DATOS_CARGADOS" not in st.session_state:
    s, ch, adn, ap = cargar_datos_maestros()
    st.session_state.SENORAS = s
    st.session_state.CHISTES = ch
    st.session_state.ADN_MAESTRO = adn
    st.session_state.APRENDIZAJES = ap
    st.session_state.DATOS_CARGADOS = True

# ==========================================
# 3. LISTA MULTIMEDIA (FOTOS Y VIDEOS)
# ==========================================
FOTOS_RANDOM = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg", "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg", "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg", "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg", "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg", "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"]
VIDEOS_RANDOM = ["https://youtu.be/sB-TdQKWMGI", "https://youtu.be/IBExxlSBbdE", "https://youtu.be/4Bt2LytMb-o", "https://youtu.be/SLhpt5vxQIw", "https://youtu.be/6Qz637nhLKc", "https://youtu.be/zBN-6NEGyzM", "https://youtu.be/leAF95qMGCg", "https://youtu.be/Rgl4n3jWGCQ"]

# ==========================================
# 4. FUNCIONES DE APOYO
# ==========================================
def sortear_sorpresa():
    st.session_state.senora = random.choice(st.session_state.SENORAS)
    st.session_state.contenido = random.choice([{"tipo": "foto", "url": f} for f in FOTOS_RANDOM] + [{"tipo": "video", "url": v} for v in VIDEOS_RANDOM])

def generar_respuesta_papi(mensaje_usuario, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt_sistema = f"""
        {st.session_state.ADN_MAESTRO}
        
        RECUERDOS Y EVENTOS RECIENTES:
        {st.session_state.APRENDIZAJES}
        
        REGLA CRÍTICA: Habla siempre de USTED. Tono tierno, protector y chileno.
        """
        mensajes = [{"role": "system", "content": prompt_sistema}]
        for m in historial[-6:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje_usuario})
        
        response = client.chat.completions.create(model="gpt-4o-mini", messages=mensajes, temperature=0.7)
        return response.choices[0].message.content
    except Exception:
        return "Pucha mi amorcito, la señal anda malita, pero aquí está su pAAPi."

# ==========================================
# 5. PANTALLA DE INICIO (PORTADA)
# ==========================================
if "acceso" in st.query_params or st.session_state.get("autenticado"):
    st.session_state.pagina = 'principal'
    st.session_state.autenticado = True
else:
    st.session_state.pagina = 'inicio'

if st.session_state.pagina == 'inicio':
    st.markdown("""<style>
        [data-testid="stAppViewContainer"] { background-color: black !important; }
        .portada-wrapper { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; display: flex; align-items: center; justify-content: center; z-index: 999; }
        .logo-sobre { position: absolute; width: 60%; max-width: 400px; z-index: 1000; }
        .stButton button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; opacity: 0; z-index: 1001; }
    </style>""", unsafe_allow_html=True)
    if st.button("ENTRAR"):
        st.session_state.autenticado = True
        sortear_sorpresa()
        st.rerun()
    st.markdown('<div class="portada-wrapper"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="width:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo-sobre"></div>', unsafe_allow_html=True)

# ==========================================
# 6. PANTALLA PRINCIPAL (CHAT)
# ==========================================
else:
    st.markdown("""<style> [data-testid="stAppViewContainer"] { background-color: white !important; } </style>""", unsafe_allow_html=True)
    
    if 'senora' not in st.session_state: st.session_state.senora = "Señora"
    if 'contenido' not in st.session_state: st.session_state.contenido = {"tipo": "foto", "url": FOTOS_RANDOM[0]}

    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.senora}!")
    
    # Mostrar Foto o Video del sorteo
    if st.session_state.contenido["tipo"] == "foto":
        st.image(st.session_state.contenido["url"], use_container_width=True)
    else:
        st.video(st.session_state.contenido["url"])

    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 14px; border-radius: 50px; text-decoration: none; font-weight: bold; width: 100%; text-align: center; display: block;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🤡 ¡Cuéntame un chiste, pAAPi!!"):
        st.info(random.choice(st.session_state.CHISTES))

    st.write("### 💬 Chat con pAAPi")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("Escriba aquí..."):
        sortear_sorpresa()
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        respuesta = generar_respuesta_papi(prompt, st.session_state.messages)
        with st.chat_message("assistant"): st.write(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.rerun()

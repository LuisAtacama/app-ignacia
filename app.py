import streamlit as st
import random
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN Y CONEXIÓN
# ==========================================
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# Conexión limpia a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# ==========================================
# 2. MOTOR DE CARGA (SIMPLIFICADO PARA EVITAR ERROR 400)
# ==========================================
def cargar_datos_maestros():
    # Valores por defecto (respaldo)
    senoras = ["Loquita", "Molita", "Señora"]
    chistes = ["— ¿Qué le dice un pan a otro pan? — Te presento una miga."]
    adn_pasado = "Eres Luis, el papá de Ignacita. Habla de USTED. Eres tierno y protector."
    aprendizajes_recientes = ""

    if conn:
        try:
            # Lectura directa sin parámetros extra para no confundir a Google
            df_s = conn.read(worksheet="Senoras")
            if df_s is not None and not df_s.empty:
                senoras = df_s.iloc[:, 0].dropna().astype(str).tolist()
            
            df_ch = conn.read(worksheet="Chistes")
            if df_ch is not None and not df_ch.empty:
                chistes = df_ch.iloc[:, 0].dropna().astype(str).tolist()
            
            df_adn = conn.read(worksheet="Contexto")
            if df_adn is not None and not df_adn.empty:
                # Junta todo el texto de la columna A
                adn_pasado = "\n".join(df_adn.iloc[:, 0].dropna().astype(str).tolist())
            
            df_ap = conn.read(worksheet="Aprendizajes")
            if df_ap is not None and not df_ap.empty:
                lista_ap = []
                for _, fila in df_ap.iterrows():
                    if len(fila) >= 2:
                        lista_ap.append(f"{fila[0]}: {fila[1]}")
                aprendizajes_recientes = "\n".join(lista_ap)
                
        except Exception as e:
            # Si falla, no bloquea la app, solo avisa
            st.warning(f"Aviso técnico: Usando memoria local. ({e})")
            
    return senoras, chistes, adn_pasado, aprendizajes_recientes

# Inicializar sesión
if "DATOS_CARGADOS" not in st.session_state:
    s, ch, adn, ap = cargar_datos_maestros()
    st.session_state.SENORAS = s
    st.session_state.CHISTES = ch
    st.session_state.ADN_MAESTRO = adn
    st.session_state.APRENDIZAJES = ap
    st.session_state.DATOS_CARGADOS = True

# ==========================================
# 3. MULTIMEDIA
# ==========================================
FOTOS_RANDOM = ["https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", "https://i.postimg.cc/44tnYt9r/ignacita-alegria-primer-oso.jpg", "https://i.postimg.cc/50wjj79Q/IMG-5005.jpg", "https://i.postimg.cc/zBn33tDg/IMG-5018.jpg", "https://i.postimg.cc/SsWjjTQz/IMG-5038.jpg", "https://i.postimg.cc/858jpQG5/IMG-5046.jpg", "https://i.postimg.cc/dV17njnY/IMG-5047.jpg", "https://i.postimg.cc/zXpbncw5/IMG-5065.jpg", "https://i.postimg.cc/02ZMpBGq/IMG-5072.jpg", "https://i.postimg.cc/TYQLr4Vz/IMG-5075.jpg", "https://i.postimg.cc/dtnk8x2n/IMG-5078.jpg", "https://i.postimg.cc/YqtLLHWF/IMG-5084.jpg", "https://i.postimg.cc/xT9NN2zJ/IMG-5093.jpg", "https://i.postimg.cc/Dy744TXW/IMG-5094.jpg", "https://i.postimg.cc/HsT88gyy/IMG-5095.jpg", "https://i.postimg.cc/FzVfCP2H/IMG-5096.jpg", "https://i.postimg.cc/br9GV6Kh/IMG-5097.jpg", "https://i.postimg.cc/rsNdZhvq/IMG-5098.jpg", "https://i.postimg.cc/Vv8rRyZH/IMG-5107.jpg", "https://i.postimg.cc/63R4n6cY/IMG-5111.jpg", "https://i.postimg.cc/ZR3vpYHL/IMG-5115.jpg", "https://i.postimg.cc/cHYtw1hm/IMG-5117.jpg", "https://i.postimg.cc/B6DPHZpj/IMG-5123.jpg", "https://i.postimg.cc/DzRbS4rL/IMG-5163.jpg", "https://i.postimg.cc/MGgjnf7S/IMG-5186.jpg", "https://i.postimg.cc/0NhJzKpT/IMG-5189.jpg", "https://i.postimg.cc/Gp4y3xyn/IMG-5204.jpg", "https://i.postimg.cc/bwCnjBdT/IMG-5214.jpg", "https://i.postimg.cc/FHWSQB1f/IMG-5215.jpg", "https://i.postimg.cc/251Zj7Zp/IMG-5239.jpg", "https://i.postimg.cc/fbV9Wf07/IMG-5241.jpg", "https://i.postimg.cc/wjTNZpqZ/IMG-5256.jpg", "https://i.postimg.cc/W1bZCvNQ/IMG-5282.jpg", "https://i.postimg.cc/FHsS84rq/IMG-5285.jpg", "https://i.postimg.cc/HksMRgYP/IMG-5290.jpg", "https://i.postimg.cc/qMGn1RTG/IMG-5291.jpg", "https://i.postimg.cc/hPnT8mHf/IMG-5295.jpg", "https://i.postimg.cc/gjVRFc6R/IMG-5324.jpg", "https://i.postimg.cc/sxdSNG1y/IMG-5365.jpg", "https://i.postimg.cc/L5Kfbg5T/IMG-5367.jpg", "https://i.postimg.cc/fynXrSyC/IMG-5371.jpg", "https://i.postimg.cc/0jRmBKjp/IMG-5378.jpg", "https://i.postimg.cc/W4y00Hvd/IMG-5384.jpg", "https://i.postimg.cc/XvqwG0tm/IMG-5395.jpg", "https://i.postimg.cc/VNvjrc27/IMG-5449.jpg", "https://i.postimg.cc/BvbxLGRV/IMG-5473.jpg", "https://i.postimg.cc/QMCp9rvq/IMG-5480.jpg", "https://i.postimg.cc/R0hc6z2G/IMG-5486.jpg", "https://i.postimg.cc/htpLtGZc/IMG-5496.jpg", "https://i.postimg.cc/VsBKnzd0/Gemini-Generated-Image-dvkezpdvkezpdvke.png"]
VIDEOS_RANDOM = ["https://youtu.be/sB-TdQKWMGI", "https://youtu.be/IBExxlSBbdE", "https://youtu.be/4Bt2LytMb-o", "https://youtu.be/SLhpt5vxQIw", "https://youtu.be/6Qz637nhLKc", "https://youtu.be/zBN-6NEGyzM", "https://youtu.be/leAF95qMGCg", "https://youtu.be/Rgl4n3jWGCQ"]

def sortear_sorpresa():
    st.session_state.senora = random.choice(st.session_state.SENORAS)
    st.session_state.contenido = random.choice([{"tipo": "foto", "url": f} for f in FOTOS_RANDOM] + [{"tipo": "video", "url": v} for v in VIDEOS_RANDOM])

# ==========================================
# 4. LÓGICA DE CHAT
# ==========================================
def generar_respuesta(mensaje, historial):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        contexto = f"{st.session_state.ADN_MAESTRO}\nRecuerdos: {st.session_state.APRENDIZAJES}"
        
        mensajes = [{"role": "system", "content": contexto}]
        for m in historial[-6:]: mensajes.append(m)
        mensajes.append({"role": "user", "content": mensaje})
        
        res = client.chat.completions.create(model="gpt-4o-mini", messages=mensajes)
        return res.choices[0].message.content
    except:
        return "Pucha mi amorcito, no pude conectarme, pero pAAPi te quiere igual."

# ==========================================
# 5. PANTALLAS
# ==========================================
if "autenticado" not in st.session_state:
    if st.button("ENTRAR (Haz clic aquí)"):
        st.session_state.autenticado = True
        sortear_sorpresa()
        st.rerun()
    st.image("https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif")
else:
    if 'senora' not in st.session_state: st.session_state.senora = "Señora"
    
    st.title(f"❤️ ¡Hola, mi Señora {st.session_state.senora}!")
    
    # Mostrar contenido del sorteo
    cont = st.session_state.contenido
    if cont["tipo"] == "foto": st.image(cont["url"], use_container_width=True)
    else: st.video(cont["url"])
    
    st.markdown(f"<a href='https://wa.me/56992238085' target='_blank' style='background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold;'>📲 HABLAR CON PAPI REAL</a>", unsafe_allow_html=True)

    st.divider()
    
    if st.button("🤡 ¡Cuéntame un chiste!"):
        st.info(random.choice(st.session_state.CHISTES))

    # Chat
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if p := st.chat_input("Dime algo..."):
        sortear_sorpresa()
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        r = generar_respuesta(p, st.session_state.messages)
        with st.chat_message("assistant"): st.write(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
        st.rerun()

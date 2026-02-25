import streamlit as st
import random
from openai import OpenAI
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="pAAPi - Ignacia Edition", page_icon="🎀", layout="centered")

# 2. FUNCIÓN DE LECTURA ROBUSTA (Busca archivos sin importar mayúsculas)
def leer_archivo_seguro(nombre_objetivo):
    # Buscamos en la carpeta actual qué archivos existen
    archivos_reales = os.listdir('.')
    archivo_encontrado = None
    
    for f in archivos_reales:
        if f.lower() == nombre_objetivo.lower():
            archivo_encontrado = f
            break
            
    if archivo_encontrado:
        try:
            with open(archivo_encontrado, "r", encoding="utf-8") as f:
                if nombre_objetivo == "adn.txt": return f.read()
                return [line.strip() for line in f.readlines() if line.strip()]
        except: pass
    
    # Valores de RESPALDO si no encuentra el archivo
    backups = {
        "adn.txt": "Eres Luis, el papá de Ignacita. Habla con mucho amor.",
        "senoras.txt": ["Loquita", "Molita", "Ignacita"],
        "chistes.txt": ["¿Qué le dice un pan a otro pan? Te presento a una miga."]
    }
    return backups.get(nombre_objetivo)

# Cargamos los datos
ADN_SISTEMA = leer_archivo_seguro("adn.txt")
APODOS = leer_archivo_seguro("senoras.txt")
LISTA_CHISTES = leer_archivo_seguro("chistes.txt")

# 3. LÓGICA DE NAVEGACIÓN (Persistencia al Refrescar)
if "entrado" not in st.session_state:
    st.session_state.entrado = False

# 4. PORTADA
if not st.session_state.entrado:
    st.markdown("""
    <style>
        .portada { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; display: flex; align-items: center; justify-content: center; z-index: 999; }
        .logo { position: absolute; width: 80%; max-width: 500px; z-index: 1000; pointer-events: none; }
        .stButton > button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: transparent !important; border: none !important; color: transparent !important; z-index: 9999 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="portada"><img src="https://i.postimg.cc/Y2R6XNTN/portada-pappi.gif" style="height:100%"><img src="https://i.postimg.cc/Bb71JpGr/image.png" class="logo"></div>', unsafe_allow_html=True)
    
    if st.button("ENTRAR", key="gate"):
        st.session_state.entrado = True
        st.session_state.mi_nombre = random.choice(APODOS)
        st.rerun()

# 5. INTERIOR
else:
    st.markdown("""
    <style>
        .stApp { background-color: white; }
        .stButton > button { position: relative !important; width: 100% !important; height: auto !important; z-index: 1 !important; background-color: #f0f2f6 !important; color: black !important; border: 1px solid #ddd !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title(f"❤️ ¡Hola, mi {st.session_state.mi_nombre}!")
    st.image("https://i.postimg.cc/gcRrxRZt/amor-papi-hija.jpg", use_container_width=True)
    
    # WhatsApp (Link directo siempre funciona)
    st.markdown('<a href="https://wa.me/56992238085" target="_blank" style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;display:block;text-align:center;font-weight:bold;margin-bottom:20px;">📲 HABLAR CON PAPI REAL</a>', unsafe_allow_html=True)
    
    if st.button("🤡 ¡Papi, cuéntame un chiste!", key="joke_btn"):
        st.info(random.choice(LISTA_CHISTES))

    st.divider()
    
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Dime algo, mi amor..."):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": ADN_SISTEMA}] + st.session_state.chat
            )
            r = res.choices[0].message.content
        except: r = "Pucha mi amor, se me cortó la señal..."
        
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.chat.append({"role": "assistant", "content": r})

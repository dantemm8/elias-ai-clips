
import streamlit as st
import re

st.set_page_config(
    page_title="Elias AI Clips",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 ELIAS AI CLIPS")
st.caption("Intelligent Video Clipping Engine")

st.markdown("---")

st.subheader("Generador inteligente de clips")

url = st.text_input(
    "🔗 Pega el enlace de YouTube",
    placeholder="https://www.youtube.com/watch?v=..."
)

cantidad = st.selectbox(
    "Cantidad de clips",
    [5, 10, 15],
    index=0
)

duracion = st.selectbox(
    "Duración de cada clip",
    [30, 45, 60],
    index=1
)

subtitulos = st.selectbox(
    "Estilo de subtítulos",
    ["Dinámicos palabra por palabra", "Normales"]
)

st.markdown("---")

st.write("### ⚙️ Configuración de video")
st.write("Formato: Vertical 9:16")
st.write("Resolución: 1080p")
st.write("Selección: Inteligencia artificial")

if st.button("🚀 PREPARAR GENERACIÓN", use_container_width=True):
    if not re.match(
        r"^https?://(www\.)?(youtube\.com|youtu\.be)/",
        url
    ):
        st.error("Introduce un enlace válido de YouTube.")
    else:
        st.success("Enlace recibido correctamente.")
        st.info(
            "La interfaz está preparada. "
            "El motor de procesamiento se conectará "
            "en la siguiente etapa."
        )
        st.write("Cantidad:", cantidad)
        st.write("Duración:", duracion, "segundos")
        st.write("Subtítulos:", subtitulos)

st.markdown("---")
st.caption("ELIAS AI CLIPS © 2026")

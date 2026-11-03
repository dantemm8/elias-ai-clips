
import streamlit as st
import re
from openai import OpenAI

st.set_page_config(
    page_title="Elias AI Clips",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 ELIAS AI CLIPS")
st.caption("INTELLIGENT VIDEO CLIPPING ENGINE")

st.divider()

st.subheader("🎥 Generador inteligente")

url = st.text_input(
    "Enlace de YouTube",
    placeholder="Pega aquí el enlace del video"
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
    ["Dinámicos", "Normales"]
)

st.divider()

st.subheader("⚙️ Configuración")

st.write("📱 Formato: Vertical 9:16")
st.write("🎞️ Resolución: 1080p")
st.write("🧠 Selección: Inteligencia artificial")

st.divider()

st.subheader("🔌 Conexión de inteligencia artificial")

if st.button("Probar conexión con OpenAI", use_container_width=True):

    try:
        api_key = st.secrets["OPENAI_API_KEY"]

        client = OpenAI(api_key=api_key)

        client.models.list()

        st.success("¡Conexión con OpenAI establecida!")

    except KeyError:
        st.error("No encontramos OPENAI_API_KEY en Secrets.")

    except Exception as e:
        st.error("No se pudo conectar con OpenAI.")
        st.code(str(e))

st.divider()

if st.button(
    "🚀 PREPARAR GENERACIÓN",
    use_container_width=True
):

    if not re.match(
        r"^https?://(www\.)?(youtube\.com|youtu\.be)/",
        url.strip()
    ):
        st.error("Introduce un enlace válido de YouTube.")

    else:
        st.success("Enlace recibido correctamente.")

        st.write("Cantidad de clips:", cantidad)
        st.write("Duración:", duracion, "segundos")
        st.write("Subtítulos:", subtitulos)

        st.info(
            "El motor de análisis y edición todavía "
            "está en construcción. Esta versión "
            "comprueba el enlace y configura el trabajo."
        )

st.divider()

st.caption("ELIAS AI CLIPS © 2026")


import streamlit as st
import os
import tempfile

from clip_pipeline import generate_clips

st.set_page_config(
    page_title="Elias AI Clips",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 ELIAS AI CLIPS")
st.caption("INTELLIGENT VIDEO CLIPPING ENGINE")

st.divider()

st.subheader("🎥 Generador inteligente")

video = st.file_uploader(
    "Sube tu video",
    type=["mp4", "mov", "mkv", "webm"]
)

cantidad = st.selectbox(
    "Cantidad de clips",
    [5, 10, 15]
)

duracion = st.selectbox(
    "Duración de cada clip",
    [30, 45, 60],
    index=1
)

st.divider()

st.write("📱 Formato: Vertical 9:16")
st.write("🎞️ Resolución: 1080 × 1920")
st.write("🧠 Selección: Inteligencia artificial")
st.write("💬 Subtítulos: Palabra por palabra")
st.write("⚡ Motor de IA: Groq")

if st.button(
    "🚀 GENERAR MIS CLIPS",
    use_container_width=True
):

    if video is None:
        st.error("Primero debes subir un video.")

    else:
        video_path = None

        try:
            api_key = st.secrets["GROQ_API_KEY"]

            extension = os.path.splitext(video.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temp_video:

                temp_video.write(video.getbuffer())
                video_path = temp_video.name

            with st.spinner(
                "La inteligencia artificial está trabajando..."
            ):

                clips = generate_clips(
                    video_path,
                    api_key,
                    cantidad,
                    duracion
                )

            if clips:
                st.success(
                    f"¡Se generaron {len(clips)} clips!"
                )

                for index, path in enumerate(clips, start=1):
                    with open(path, "rb") as file:
                        st.download_button(
                            f"⬇️ Descargar clip {index}",
                            data=file.read(),
                            file_name=os.path.basename(path),
                            mime="video/mp4",
                            key=f"download_{index}"
                        )
            else:
                st.warning(
                    "No se pudieron generar clips válidos."
                )

        except Exception as error:
            st.error("Ocurrió un error durante la generación.")
            st.code(str(error))

        finally:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)

st.divider()
st.caption("ELIAS AI CLIPS © 2026")

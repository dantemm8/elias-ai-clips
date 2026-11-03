import subprocess
import os


def extract_audio(video_path, output_path="audio.mp3"):
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-b:a", "64k",
        output_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "No se pudo extraer el audio: " + result.stderr
        )

    if not os.path.exists(output_path):
        raise RuntimeError("No se generó el archivo de audio.")

    return output_path

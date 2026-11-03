import subprocess
import os


def create_clip(video_path, start, end, output_path):
    duration = end - start

    if duration <= 0:
        raise ValueError("La duración del clip no es válida.")

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-i", video_path,
        "-t", str(duration),
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Error al crear el clip: " + result.stderr
        )

    if not os.path.exists(output_path):
        raise RuntimeError("No se generó el clip.")

    return output_path

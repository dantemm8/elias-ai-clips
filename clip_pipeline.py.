import os
import subprocess
import tempfile

from audio_extractor import extract_audio
from transcriber import transcribe_audio
from clip_selector import select_best_clips
from video_editor import create_clip
from subtitle_generator import create_subtitles


def generate_clips(
    video_path,
    api_key,
    quantity=5,
    duration=45
):
    output_dir = "generated_clips"
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:

        audio_path = os.path.join(temp_dir, "audio.mp3")

        extract_audio(video_path, audio_path)

        if os.path.getsize(audio_path) > 24 * 1024 * 1024:
            raise ValueError(
                "El audio supera el límite de 24 MB. "
                "Necesitamos dividirlo antes de transcribirlo."
            )

        transcription = transcribe_audio(
            audio_path,
            api_key
        )

        selection = select_best_clips(
            transcription,
            api_key,
            quantity,
            duration
        )

        words = transcription.get("words", [])
        created_files = []

        for index, clip in enumerate(selection["clips"], start=1):

            start = float(clip["start"])
            end = float(clip["end"])

            if end <= start:
                continue

            if end - start > duration + 5:
                end = start + duration

            clip_words = [
                word for word in words
                if float(word["start"]) >= start
                and float(word["end"]) <= end
            ]

            if not clip_words:
                continue

            subtitle_path = os.path.join(
                temp_dir,
                f"subtitles_{index}.ass"
            )

            create_subtitles(
                clip_words,
                subtitle_path,
                clip_start=start
            )

            silent_clip_path = os.path.join(
                temp_dir,
                f"clip_{index}.mp4"
            )

            final_clip_path = os.path.join(
                output_dir,
                f"elias_clip_{index}.mp4"
            )

            create_clip(
                video_path,
                start,
                end,
                silent_clip_path
            )

            command = [
                "ffmpeg",
                "-y",
                "-i", silent_clip_path,
                "-vf", f"ass={subtitle_path}",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-c:a", "copy",
                "-movflags", "+faststart",
                final_clip_path
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(
                    "Error al añadir subtítulos: "
                    + result.stderr
                )

            created_files.append(final_clip_path)

    return created_files

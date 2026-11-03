
import os
import subprocess
import tempfile

from audio_extractor import extract_audio
from transcriber import transcribe_audio
from clip_selector import select_best_clips
from video_editor import create_clip
from subtitle_generator import create_subtitles


def split_audio(audio_path, output_dir, chunk_seconds=600):
    output_pattern = os.path.join(
        output_dir,
        "audio_part_%03d.mp3"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-c", "copy",
        output_pattern
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "No se pudo dividir el audio: " + result.stderr
        )

    return sorted([
        os.path.join(output_dir, file)
        for file in os.listdir(output_dir)
        if file.startswith("audio_part_")
        and file.endswith(".mp3")
    ])


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

        audio_parts = split_audio(audio_path, temp_dir)

        complete_transcription = {
            "text": "",
            "segments": [],
            "words": []
        }

        time_offset = 0

        for part_path in audio_parts:

            if os.path.getsize(part_path) > 24 * 1024 * 1024:
                raise ValueError(
                    "Una parte del audio supera 24 MB. "
                    "Reduce la duración de los segmentos."
                )

            transcription = transcribe_audio(
                part_path,
                api_key
            )

            complete_transcription["text"] += (
                transcription["text"] + " "
            )

            for segment in transcription["segments"]:
                complete_transcription["segments"].append({
                    "start": segment["start"] + time_offset,
                    "end": segment["end"] + time_offset,
                    "text": segment["text"]
                })

            for word in transcription["words"]:
                complete_transcription["words"].append({
                    "start": word["start"] + time_offset,
                    "end": word["end"] + time_offset,
                    "text": word["text"]
                })

            probe = subprocess.run(
                [
                    "ffprobe",
                    "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    part_path
                ],
                capture_output=True,
                text=True
            )

            time_offset += float(probe.stdout.strip())

        selection = select_best_clips(
            complete_transcription,
            api_key,
            quantity,
            duration
        )

        words = complete_transcription["words"]
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

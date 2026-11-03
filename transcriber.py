
from groq import Groq


def get_value(item, key):
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key, None)


def transcribe_audio(audio_path, api_key):
    client = Groq(api_key=api_key)

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment", "word"]
        )

    segments = get_value(transcription, "segments") or []
    words = get_value(transcription, "words") or []

    return {
        "text": get_value(transcription, "text") or "",
        "segments": [
            {
                "start": float(get_value(segment, "start")),
                "end": float(get_value(segment, "end")),
                "text": get_value(segment, "text") or ""
            }
            for segment in segments
        ],
        "words": [
            {
                "start": float(get_value(word, "start")),
                "end": float(get_value(word, "end")),
                "text": get_value(word, "word") or get_value(word, "text") or ""
            }
            for word in words
        ]
    }

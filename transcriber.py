from openai import OpenAI


def transcribe_audio(audio_path, api_key):
    client = OpenAI(api_key=api_key)

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment", "word"]
        )

    return {
        "text": transcription.text,
        "segments": [
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
            for segment in transcription.segments
        ],
        "words": [
            {
                "start": word.start,
                "end": word.end,
                "text": word.word
            }
            for word in transcription.words
        ]
    }

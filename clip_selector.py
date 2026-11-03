
import json
from groq import Groq


def select_best_clips(
    transcription,
    api_key,
    quantity=5,
    duration=45
):
    client = Groq(api_key=api_key)

    segments = transcription.get("segments", [])

    if not segments:
        raise ValueError(
            "La transcripción no contiene tiempos."
        )

    timestamped_text = "\n".join(
        f"[{item['start']:.2f} - {item['end']:.2f}] "
        f"{item['text']}"
        for item in segments
    )

    prompt = f"""
Eres un editor profesional de TikTok,
Instagram Reels y YouTube Shorts.

Selecciona exactamente {quantity} momentos
interesantes de esta transcripción.

Duración objetivo de cada clip: {duration} segundos.

Prioriza:
- Ganchos que atrapen desde el inicio.
- Historias completas.
- Revelaciones y sorpresas.
- Consejos útiles.
- Emociones y momentos impactantes.

Evita repeticiones y fragmentos sin contexto.

Devuelve exclusivamente un JSON con esta estructura:

{{
  "clips": [
    {{
      "start": 10.5,
      "end": 55.5,
      "hook": "Gancho del clip",
      "reason": "Motivo de selección"
    }}
  ]
}}

Los tiempos deben estar en segundos y dentro
de los límites de la transcripción.
No inventes marcas de tiempo.

TRANSCRIPCIÓN CON TIEMPOS:
{timestamped_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Eres un editor experto en videos cortos."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(
        response.choices[0].message.content
    )

    return result

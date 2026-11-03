
import json
from openai import OpenAI

def select_best_clips(transcript, quantity=5, duration=45):

    client = OpenAI()

    prompt = f"""
    Eres un experto editor de videos cortos para TikTok,
    Instagram Reels y YouTube Shorts.

    Analiza esta transcripción y selecciona los
    {quantity} mejores momentos.

    Cada clip debe durar aproximadamente {duration} segundos.

    Prioriza:
    - Frases que atrapen desde el principio.
    - Historias interesantes.
    - Revelaciones y sorpresas.
    - Consejos útiles.
    - Momentos emocionales.
    - Fragmentos que tengan sentido por sí solos.

    Evita:
    - Repeticiones.
    - Silencios.
    - Fragmentos sin contexto.
    - Momentos aburridos.

    Devuelve exclusivamente JSON con esta estructura:

    {{
      "clips": [
        {{
          "start": 0,
          "end": 45,
          "hook": "Gancho del video",
          "reason": "Por qué seleccionaste este momento"
        }}
      ]
    }}

    TRANSCRIPCIÓN:
    {transcript}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un editor profesional de videos virales."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(
        response.choices[0].message.content
    )

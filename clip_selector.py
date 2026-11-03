
import json
from openai import OpenAI

def select_best_clips(
    transcript,
    api_key,
    quantity=5,
    duration=45
):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    Eres un editor profesional de TikTok,
    Reels y YouTube Shorts.

    Analiza esta transcripción y selecciona
    exactamente {quantity} momentos.

    Duración objetivo: {duration} segundos.

    Prioriza:
    - Ganchos impactantes.
    - Historias completas.
    - Revelaciones.
    - Consejos interesantes.
    - Emociones y sorpresas.

    Evita repeticiones y fragmentos sin contexto.

    Devuelve JSON con esta estructura:

    {{
      "clips": [
        {{
          "start": 0,
          "end": 45,
          "hook": "Gancho",
          "reason": "Motivo de selección"
        }}
      ]
    }}

    Los tiempos deben corresponder a la transcripción.
    No inventes marcas de tiempo.

    TRANSCRIPCIÓN:
    {transcript}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
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

    return json.loads(
        response.choices[0].message.content
    )

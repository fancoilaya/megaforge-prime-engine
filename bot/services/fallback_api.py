# bot/services/fallback_api.py

import requests
import uuid
import urllib.parse
from bot.utils.style import MEGAGROK_STYLE


def generate_fallback_image(prompt: str) -> str:
    """Stable fallback using Pollinations simple endpoint."""

    # Combine style + user idea in one strong prompt
    final_prompt = f"{MEGAGROK_STYLE}. {prompt}"

    encoded = urllib.parse.quote(final_prompt)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=768&height=768&nologo=true&model=series1"
    )

    print("Fallback request:", url)

    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        raise Exception(f"Fallback generator error {response.status_code}")

    output_path = f"/tmp/{uuid.uuid4()}.jpg"

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

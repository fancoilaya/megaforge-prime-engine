# bot/services/fallback_api.py

import requests
import uuid
import base64
from bot.utils.style import MEGAGROK_STYLE

def generate_fallback_image(prompt: str) -> str:
    """Free fallback using Pollinations.io"""

    final_prompt = f"{MEGAGROK_STYLE}\nUser idea: {prompt}"

    url = (
        "https://image.pollinations.ai/prompt/"
        + requests.utils.quote(final_prompt)
        + "?width=768&height=768&nologo=true"
    )

    print("Fallback request:", url)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Fallback generator error {response.status_code}")

    # ---- FIXED INDENTATION BELOW ----
    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

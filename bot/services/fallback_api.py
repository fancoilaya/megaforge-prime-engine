# bot/services/fallback_api.py

import requests
import uuid
import base64
from bot.utils.style import MEGAGROK_STYLE

def clean_prompt(text: str) -> str:
    """Pollinations breaks if prompt contains newlines or special chars."""
    return " ".join(text.split())  # removes line breaks

def generate_fallback_image(prompt: str) -> str:
    """Free fallback using Pollinations.io"""

    # Merge prompt with style
    final_prompt = f"{MEGAGROK_STYLE} {prompt}"
    final_prompt = clean_prompt(final_prompt)

    url_prompt = requests.utils.quote(final_prompt)

    url = (
        f"https://image.pollinations.ai/prompt/{url_prompt}"
        f"?width=768&height=768&nologo=true"
    )

    print("Fallback request:", url)

    headers = {
        "User-Agent": "Mozilla/5.0"  # required, otherwise 404 occurs
    }

    response = requests.get(url, headers=headers)

    # If Pollinations returns JSON instead of an image (rare)
    if response.status_code == 404:
        raise Exception("Pollinations returned 404 — prompt rejected")

    if response.status_code != 200:
        raise Exception(f"Fallback generator error {response.status_code}")

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

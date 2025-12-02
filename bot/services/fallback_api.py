# bot/services/fallback_api.py

import requests
import uuid
import os
from bot.utils.style import MEGAGROK_STYLE

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"

# Pollinations cannot handle long text URLs → compress style prompt
COMPRESSED_STYLE = (
    "MegaGrok frog hero, 1970s comic poster, strong black outlines, "
    "halftone texture, bold colors, heroic stance, vintage monster comic style."
)

def generate_fallback_image(prompt: str) -> str:
    """
    Free fallback using Pollinations.io
    Uses a compressed style for stability (long URLs cause 404).
    """

    # Build short final prompt
    final_prompt = f"{COMPRESSED_STYLE}. {prompt}"

    encoded = requests.utils.quote(final_prompt)

    url = f"{POLLINATIONS_URL}{encoded}?width=768&height=768&nologo=true"

    print("Fallback request:", url)

    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        raise Exception(f"Fallback generator error {response.status_code}")

    # Save image
    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

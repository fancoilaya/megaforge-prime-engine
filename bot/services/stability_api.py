# bot/services/stability_api.py

import requests
import uuid
import os
import base64
from bot.config import STABILITY_API_KEY
from PIL import Image
import io

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

print(">>> Stability module loaded:", __file__)
print(">>> Using API KEY:", "SET" if STABILITY_API_KEY else "MISSING")
print(">>> Endpoint:", API_URL)

def generate_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1"),
    }

    response = requests.post(API_URL, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(
            f"Stability API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    if "images" not in data or len(data["images"]) == 0:
        raise Exception("Stability error: missing 'images' in response")

    image_b64 = data["images"][0]["image"]
    image_bytes = base64.b64decode(image_b64)

    # ---------------------------
    # 🔥 NEW IMAGE COMPRESSION 🔥
    # ---------------------------
    img = Image.open(io.BytesIO(image_bytes))

    # Resize max 768x768
    img.thumbnail((768, 768))

    # Convert to JPG (much smaller than PNG)
    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=85)

    return output_path

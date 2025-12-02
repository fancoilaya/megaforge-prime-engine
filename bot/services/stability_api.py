# bot/services/stability_api.py

import requests
import uuid
import base64
import os
from PIL import Image
import io

from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"


def generate_image(prompt: str) -> str:
    print("\n==============================")
    print("🟦 STABILITY DEBUG MODE ACTIVE")
    print("==============================")
    print("👉 FINAL PROMPT SENT TO STABILITY:\n")
    print(prompt)
    print("\n==============================\n")

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1"),
    }

    # Actual API request
    response = requests.post(API_URL, headers=headers, files=files)

    print("🟧 RAW STATUS CODE:", response.status_code)
    print("🟪 RAW RESPONSE TEXT:")
    print(response.text[:1000])  # prevent huge logs

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    # Extract image
    data = response.json()

    if "image" in data:
        # New endpoint format
        image_b64 = data["image"]
    elif "images" in data and len(data["images"]) > 0:
        image_b64 = data["images"][0]["image"]
    else:
        raise Exception("Stability error: missing 'image' or 'images' in response")

    image_bytes = base64.b64decode(image_b64)

    # Convert & compress to JPG
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((768, 768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=90)

    print("✅ IMAGE GENERATED AT:", output_path)
    print("==============================\n")

    return output_path

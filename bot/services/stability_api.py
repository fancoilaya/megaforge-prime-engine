# bot/services/stability_api.py  (FIXED FOR v2 CORE)

import requests
import uuid
import base64
import io
from PIL import Image

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
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "core",
        "prompt": {
            "text": prompt
        },
        "aspect_ratio": "1:1",
        "output_format": "jpeg",
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    print("🟧 RAW STATUS CODE:", response.status_code)
    print("🟪 RAW RESPONSE TEXT:")
    print(response.text[:1000])

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    data = response.json()

    # Stability v2 ALWAYS returns data["image"]
    if "image" not in data:
        raise Exception("Stability error: missing 'image' in response")

    image_bytes = base64.b64decode(data["image"])

    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((768,768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=90)

    print("✅ IMAGE GENERATED AT:", output_path)
    print("==============================\n")

    return output_path

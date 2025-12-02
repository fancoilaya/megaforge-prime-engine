# bot/services/stability_api.py  
# Correct multipart/form-data implementation for Stability T2I API

import requests
import uuid
import base64
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
        # DO NOT set Content-Type yourself
    }

    files = {
        "prompt": (None, prompt),
        "aspect_ratio": (None, "1:1"),
        "output_format": (None, "jpeg"),
        # REQUIRED FIX → add strength even for text-only prompts
        "strength": (None, "1.0"),
    }

    response = requests.post(API_URL, headers=headers, files=files)

    print("🟧 RAW STATUS CODE:", response.status_code)
    print("🟪 RAW RESPONSE TEXT:")
    print(response.text[:1000])

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    data = response.json()

    if "image" not in data:
        raise Exception("Stability error: missing 'image' in response")

    image_bytes = base64.b64decode(data["image"])
    file_path = f"/tmp/{uuid.uuid4()}.jpg"

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    print("✅ IMAGE SAVED:", file_path)
    return file_path

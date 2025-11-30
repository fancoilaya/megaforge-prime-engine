import requests
import uuid
import os
import base64

from bot.config import STABILITY_API_KEY


def generate_image(prompt: str) -> str:
    # ✅ Correct Stability Creative endpoint
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "output_format": "png",
        "aspect_ratio": "1:1"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(
            f"Stability API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Stability returns base64 under images[0].image
    image_b64 = data["images"][0]["image"]
    image_bytes = base64.b64decode(image_b64)

    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

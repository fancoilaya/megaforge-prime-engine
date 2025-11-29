# bot/services/stability_api.py
import requests
import uuid
import base64
from bot.config import STABILITY_API_KEY


def generate_image(prompt: str) -> str:
    url = "https://api.stability.ai/v2beta/image/generate"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "output_format": "png"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Stability API error: {response.status_code} | {response.text}")

    data = response.json()

    # Stability now returns base64 inside "image" field
    image_base64 = data["image"]
    image_bytes = base64.b64decode(image_base64)

    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path


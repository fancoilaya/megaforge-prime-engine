import requests
import uuid
import os
from bot.config import STABILITY_API_KEY

def generate_image(prompt: str) -> str:
    url = "https://api.stability.ai/v2beta/stable-image/generate/standard"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    image_base64 = data["image"]

    # Decode
    import base64
    image_bytes = base64.b64decode(image_base64)

    # Save
    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

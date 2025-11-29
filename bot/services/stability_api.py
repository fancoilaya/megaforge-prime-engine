# bot/services/stability_api.py

import requests
import uuid
import os
import base64
from bot.config import STABILITY_API_KEY


def generate_image(prompt: str) -> str:
    """
    Generate an image using Stability AI’s v2beta API.
    Returns the local file path to the generated PNG.
    """

    url = "https://api.stability.ai/v2beta/image/generate"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "stable-diffusion-3-medium",   # REQUIRED MODEL NAME
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "output_format": "png",
    }

    response = requests.post(url, json=payload, headers=headers)

    # If Stability returns a non-200, show full error details
    if response.status_code != 200:
        raise Exception(
            f"Stability API error: {response.status_code} | {response.text}"
        )

    data = response.json()

    # Stability returns the image under the key "image"
    if "image" not in data:
        raise Exception("Stability API did not return an image")

    image_bytes = base64.b64decode(data["image"])

    # Save to /tmp (Render supports this location)
    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

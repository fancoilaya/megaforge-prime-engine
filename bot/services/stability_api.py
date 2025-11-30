import requests
import uuid
import os
import base64

from bot.config import STABILITY_API_KEY


def generate_image(prompt: str) -> str:
    url = "https://api.stability.ai/v2beta/image/generate/creative"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    payload = {
        "prompt": prompt,
        "output_format": "png",
        "aspect_ratio": "1:1"
    }

    response = requests.post(url, headers=headers, json=payload)

    # If API throws an error, we surface the message
    if response.status_code != 200:
        raise Exception(
            f"Stability API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Their new API returns images under "images":[{"image":"<base64>"}]
    image_b64 = data["images"][0]["image"]

    image_bytes = base64.b64decode(image_b64)

    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

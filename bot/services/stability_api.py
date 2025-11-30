import requests
import uuid
import os
import base64

from bot.config import STABILITY_API_KEY

print(">>> Stability module loaded:", __file__)
print(">>> Using API KEY:", "SET" if STABILITY_API_KEY else "MISSING")
print(">>> Endpoint:", "https://api.stability.ai/v2beta/stable-image/generate/creative")

def generate_image(prompt: str) -> str:
    url = "https://api.stability.ai/v2beta/stable-image/generate/creative"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    # REQUIRED FIELDS per Stability docs
    files = {
        "prompt": (None, prompt),
        "mode": (None, "prompt"),        # THIS IS REQUIRED
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(
            f"Stability API Error {response.status_code}: {response.text}"
        )

    data = response.json()
    image_b64 = data["images"][0]["image"]

    image_bytes = base64.b64decode(image_b64)

    path = f"/tmp/{uuid.uuid4()}.png"

    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

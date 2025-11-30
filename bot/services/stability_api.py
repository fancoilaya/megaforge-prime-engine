# bot/services/stability_api.py

import requests
import uuid
import os
import base64

from bot.config import STABILITY_API_KEY

# DEBUG — this will show in Render logs so we know exactly which file is being used
print(">>> USING stability_api FROM:", __file__)
print(">>> USING Stability Creative Endpoint:", "https://api.stability.ai/v2beta/stable-image/generate/creative")


def generate_image(prompt: str) -> str:
    """
    Generate an image using Stability AI Creative endpoint.
    Endpoint requires multipart/form-data, not JSON.
    """

    url = "https://api.stability.ai/v2beta/stable-image/generate/creative"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    # multipart/form-data payload
    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1"),
    }

    response = requests.post(url, headers=headers, files=files)

    # Debug network errors
    if response.status_code != 200:
        raise Exception(
            f"Stability API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Extract base64 from correct response format
    image_b64 = data["images"][0]["image"]
    image_bytes = base64.b64decode(image_b64)

    # Save image
    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

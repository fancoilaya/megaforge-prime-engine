import requests
import uuid
import os
import base64
from bot.config import STABILITY_API_KEY


def generate_image(prompt: str) -> str:
    """
    Generate an image using Stability AI's updated v2beta API.
    Saves the output to /tmp and returns file path.
    """

    url = "https://api.stability.ai/v2beta/image/generate"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/png",
    }

    # Stability API now uses multipart/form-data, not JSON.
    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1"),
        "mode": (None, "text-to-image"),
    }

    response = requests.post(url, headers=headers, files=files)

    # Raise error if any
    try:
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Stability API error: {response.text}")

    # Save returned PNG file
    image_path = f"/tmp/{uuid.uuid4()}.png"

    with open(image_path, "wb") as f:
        f.write(response.content)

    return image_path

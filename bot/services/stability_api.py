# bot/services/stability_api.py

import requests
import uuid
import io
from PIL import Image
from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"


def generate_image(prompt: str) -> str:
    """
    Sends a correct multipart/form-data image generation request
    to Stability AI using the v2beta core endpoint.
    """

    # ----- HEADERS -----
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*",  # Stability requires image/* or application/json
    }

    # ----- FORM FIELDS -----
    data = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "output_format": "png",
        # You CAN add:
        # "negative_prompt": "...",
        # "style_preset": "comic-book",
        # "seed": "0",
    }

    # ----- REQUIRED TRICK -----
    # Stability requires *at least one file* in the multipart request.
    # They suggest sending a dummy form part:
    files = {"none": ("", "")}

    print("\n===== STABILITY REQUEST DEBUG =====")
    print("URL:", API_URL)
    print("HEADERS:", headers)
    print("DATA:", data)
    print("FILES:", files)
    print("===================================\n")

    response = requests.post(API_URL, headers=headers, data=data, files=files)

    # If error:
    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    # Process returned image (PNG)
    img_bytes = response.content
    img = Image.open(io.BytesIO(img_bytes))

    # Resize for Telegram
    img.thumbnail((768, 768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=95)

    return output_path

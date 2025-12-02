import requests
import uuid
import base64
import io
from PIL import Image
from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

def generate_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*"     # ✅ Stability requires image/* or application/json
    }

    # MUST be multipart/form-data
    files = {
        "prompt": (None, prompt)
    }

    response = requests.post(API_URL, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    # Response is binary image (PNG)
    img_bytes = response.content

    # convert → JPEG (smaller for Telegram)
    img = Image.open(io.BytesIO(img_bytes))
    img.thumbnail((768, 768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=90)

    return output_path

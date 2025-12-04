import requests
import uuid
import io
import base64
from PIL import Image
from bot.config import STABILITY_API_KEY

# Stability Core endpoint
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

# Enable or disable debug prints
DEBUG = True


def generate_image(prompt: str) -> str:
    """
    Generates an image using Stability v2beta Core API.
    Fully compliant with official docs:
    https://platform.stability.ai/docs/api-reference#tag/Generate/paths/~1v2beta~1stable-image~1generate~1core/post
    """

    # Required headers
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*",        # MUST be image/* or application/json
    }

    # Must use multipart/form-data → files + data
    files = {
        "none": (None, "")          # required dummy part
    }

    # Body values (Stability reads ONLY from "data")
    data = {
        "prompt": prompt,
        "output_format": "png",     # png → best detail
        "aspect_ratio": "1:1",      # stable and predictable
        # "style_preset": "comic-book",  # optional preset
        # "seed": 0,                    # optional
    }

    if DEBUG:
        print("======================")
        print("🔵 STABILITY REQUEST")
        print("======================")
        print("URL:", API_URL)
        print("HEADERS:", headers)
        print("FILES:", files)
        print("DATA:", data)
        print("======================")

    # Send POST request
    response = requests.post(
        API_URL,
        headers=headers,
        files=files,
        data=data,
        timeout=90
    )

    # Handle API errors
    if response.status_code != 200:
        try:
            err = response.json()
        except Exception:
            err = response.text

        raise Exception(f"Stability API Error {response.status_code}: {err}")

    # Response is a PNG binary blob
    image_bytes = response.content

    # Convert to JPEG (Telegram friendly & stable)
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((768, 768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=90)

    if DEBUG:
        print("======================")
        print("🔵 STABILITY RESPONSE OK")
        print("======================")
        print("Saved to:", output_path)
        print("======================\n")

    return output_path

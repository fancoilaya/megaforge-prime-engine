import requests
import uuid
import io
from PIL import Image
from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

def generate_image(prompt: str) -> str:
    """
    Correct Stability 'core' endpoint implementation.
    MUST use:
        files = { "none": "" }
        data = { "prompt": "...", "output_format": "png" }
    """

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*"
    }

    # Required weird Stability form format
    files = {
        "none": ""
    }

    data = {
        "prompt": prompt,
        "output_format": "png"
    }

    response = requests.post(API_URL, headers=headers, files=files, data=data)

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    # Response is a PNG image
    img_bytes = response.content

    img = Image.open(io.BytesIO(img_bytes))
    img.thumbnail((768, 768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=90)

    return output_path

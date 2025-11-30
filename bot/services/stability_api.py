import requests
import uuid
import base64
from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

print(">>> Stability module loaded:", __file__)
print(">>> Using API KEY:", "SET" if STABILITY_API_KEY else "MISSING")
print(">>> Endpoint:", API_URL)

def generate_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    # Required multipart/form-data fields for CORE endpoint
    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1"),
    }

    response = requests.post(API_URL, headers=headers, files=files)

    # Log raw response for debugging
    print(">>> Stability RAW Response:", response.text)

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    data = response.json()

    if "images" not in data:
        raise Exception(f"Stability error: missing 'images' → {data}")

    image_b64 = data["images"][0]["image"]
    image_bytes = base64.b64decode(image_b64)

    # Save file to /tmp
    path = f"/tmp/{uuid.uuid4()}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

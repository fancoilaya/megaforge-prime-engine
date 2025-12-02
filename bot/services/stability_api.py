import requests
import uuid

from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

def generate_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/png",  # or "image/*"
    }
    data = {
        "prompt": prompt,
        # optionally "aspect_ratio": "1:1",
        # optionally "output_format": "png",
    }
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")
    file_path = f"/tmp/{uuid.uuid4()}.png"
    with open(file_path, "wb") as f:
        f.write(response.content)
    return file_path

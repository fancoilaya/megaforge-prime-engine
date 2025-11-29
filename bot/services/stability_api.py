# bot/services/stability_api.py

import requests
import os

API_KEY = os.getenv("STABILITY_API_KEY")

def generate_image(prompt: str) -> str:
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    data = {
        "prompt": prompt,
        "output_format": "png"
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()

    image_bytes = bytes(result["image"], "utf-8")
    output_path = "/tmp/generated.png"

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path

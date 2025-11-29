import requests, uuid, os
from bot.config import STABILITY_API_KEY


OUTPUT_DIR = "bot/storage/generated/"




def generate_image(prompt):
url = "https://api.stability.ai/v2beta/stable-image/generate/standard"


headers = {"Authorization": f"Bearer {STABILITY_API_KEY}"}
payload = {
"prompt": prompt,
"output_format": "png",
"aspect_ratio": "1:1"
}


response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()


image_bytes = response.content
filename = f"{OUTPUT_DIR}{uuid.uuid4()}.png"
with open(filename, "wb") as f:
f.write(image_bytes)


return filename

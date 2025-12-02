import requests
import uuid
import io
from PIL import Image
from bot.config import STABILITY_API_KEY

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

DEBUG_MODE = True  # 🔥 Turn on/off Stability debug logging


def debug_print(msg: str):
    """Print debug messages in Render logs."""
    if DEBUG_MODE:
        print("\n================ STABILITY DEBUG ================")
        print(msg)
        print("=================================================\n")


def generate_image(prompt: str) -> str:
    """
    Correct Stability CORE endpoint using:
        files = { "none": "" }
        data  = { prompt, output_format }
    """

    # -------------------------
    # 🔥 DEBUG: Print final prompt
    # -------------------------
    debug_print(f"FINAL PROMPT SENT TO STABILITY:\n{prompt}")

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*"  # MUST be image/*
    }

    # Required weird multipart field
    files = {
        "none": ""
    }

    data = {
        "prompt": prompt,
        "output_format": "png"
    }

    # -------------------------
    # 🔥 DEBUG: Print outgoing request info
    # -------------------------
    debug_print(
        f"SENDING REQUEST TO: {API_URL}\n\n"
        f"HEADERS:\n{headers}\n\n"
        f"FILES:\n{files}\n\n"
        f"DATA:\n{data}\n"
    )

    response = requests.post(API_URL, headers=headers, files=files, data=data)

    # -------------------------
    # 🔥 DEBUG: Log status + text
    # -------------------------
    txt = response.text[:500] if response.text else "<no text>"
    debug_print(f"STATUS: {response.status_code}\nRESPONSE BODY (first 500 chars):\n{txt}")

    if response.status_code != 200:
        raise Exception(f"Stability API Error {response.status_code}: {response.text}")

    # Response is PNG
    img_bytes = response.content

    img = Image.open(io.BytesIO(img_bytes))
    img.thumbnail((768, 768))

    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(output_path, "JPEG", quality=90)

    debug_print(f"IMAGE SAVED TO: {output_path}")

    return output_path

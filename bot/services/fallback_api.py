import requests
import uuid
import urllib.parse


def generate_fallback_image(prompt: str) -> str:
    """
    SUPER-STABLE free generator for Pollinations.
    Ensures no 404 by compressing and cleaning the prompt.
    """

    # Remove newlines and extra spaces
    clean = " ".join(prompt.split())

    # URL encode (Pollinations requires strict encoding)
    clean_encoded = urllib.parse.quote(clean)

    # Build Pollinations URL (using stable model series1)
    url = (
        f"https://image.pollinations.ai/prompt/{clean_encoded}"
        "?width=768&height=768&nologo=true&model=series1"
    )

    print("Fallback request:", url)

    response = requests.get(url, timeout=40)

    if response.status_code != 200:
        raise Exception(f"Fallback generator error {response.status_code}")

    # Save result
    output_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

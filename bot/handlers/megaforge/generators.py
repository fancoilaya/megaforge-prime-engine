import random

from bot.services.fallback_api import generate_fallback_image
from bot.services.stability_api import generate_image as generate_stability_image


# Internal style pool (procedural chaos, not static)
STYLE_POOL = [
    "comic book style, bold outlines, vibrant colors",
    "dark comic noir, dramatic lighting, graphic novel",
    "hyper expressive comic art, exaggerated emotions",
    "clean comic panels, modern western comic style",
    "high contrast comic illustration, dynamic action pose",
]


def _random_style():
    return random.choice(STYLE_POOL)


async def generate_image(prompt: str, is_vip: bool) -> str:
    """
    Main image generator.
    VIP → Stability
    Free → Fallback (Pollinations)
    """

    final_prompt = f"{prompt}, {_random_style()}"

    if is_vip:
        return await generate_stability_image(final_prompt)

    # fallback API is SYNC → do NOT await
    return generate_fallback_image(final_prompt)


async def generate_chaos_image(is_vip: bool) -> str:
    """
    Pure procedural chaos generator.
    """

    chaos_prompts = [
        "MegaGrok breaking the fourth wall inside a comic",
        "MegaGrok as a cosmic entity tearing through panels",
        "MegaGrok laughing while reality glitches around him",
        "MegaGrok forged from pure chaos energy",
        "MegaGrok as a comic god rewriting the page",
    ]

    prompt = random.choice(chaos_prompts)
    final_prompt = f"{prompt}, {_random_style()}"

    if is_vip:
        return await generate_stability_image(final_prompt)

    return generate_fallback_image(final_prompt)

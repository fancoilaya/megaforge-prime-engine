import random

from bot.services.stability_api import generate_image as generate_stability_image
from bot.services.fallback_api import generate_fallback_image


# -----------------------------
# CHAOS PROMPTS
# -----------------------------
CHAOS_PROMPTS = [
    "MegaGrok breaking the fourth wall inside a comic",
    "Grok as a chaotic trickster god in a neon comic universe",
    "MegaGrok laughing while reality glitches around him",
    "A comic panel tearing itself apart, Grok emerging",
    "Absurd comic chaos, bold colors, surreal action",
]


def random_chaos_prompt(style: str | None = None) -> str:
    base = random.choice(CHAOS_PROMPTS)

    if style:
        return f"{base}, {style}, comic book style, bold outlines, vibrant colors"

    return f"{base}, comic book style, bold outlines, vibrant colors"


# -----------------------------
# IMAGE GENERATORS
# -----------------------------
async def generate_image(prompt: str, is_vip: bool) -> str:
    """
    Standard image generation.
    VIP -> Stability (async)
    Free -> Pollinations (sync)
    """
    if is_vip:
        return await generate_stability_image(prompt)

    return generate_fallback_image(prompt)


async def generate_chaos_image(is_vip: bool, style: str | None = None) -> str:
    """
    Chaos generator with random prompt.
    """
    chaos_prompt = random_chaos_prompt(style)

    if is_vip:
        return await generate_stability_image(chaos_prompt)

    return generate_fallback_image(chaos_prompt)

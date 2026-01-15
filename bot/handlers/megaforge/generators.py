import random
from bot.services.fallback_api import generate_fallback_image
from bot.services.stability_api import generate_image as generate_stability_image


STYLE_POOL = [
    "comic book style, bold outlines, vibrant colors",
    "dark comic noir, dramatic lighting, graphic novel",
    "hyper expressive comic art, exaggerated emotions",
    "modern western comic illustration, clean panels",
    "high contrast comic art, dynamic action pose",
]


def _random_style() -> str:
    return random.choice(STYLE_POOL)


async def generate_image(prompt: str, is_vip: bool) -> str:
    """
    Always inject MegaGrok into the prompt.
    VIP → Stability
    Free → Pollinations fallback
    """
    print(
        "MEGAFORGE GENERATOR MODE:",
        "VIP / STABILITY" if is_vip else "FREE / POLLINATIONS"
    )

    style = _random_style()

    final_prompt = (
        f"MegaGrok character, {prompt}, "
        f"comic universe, {style}"
    )

    if is_vip:
        return generate_stability_image(final_prompt)

    # fallback is synchronous
    return generate_fallback_image(final_prompt)

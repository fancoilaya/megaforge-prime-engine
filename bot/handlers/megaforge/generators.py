import random
from bot.services.stability_api import generate_stability_image
from bot.services.fallback_api import generate_pollinations_image

# -----------------------------
# FREE PROMPT IMAGE
# -----------------------------
async def generate_image(prompt: str, is_vip: bool) -> str:
    final_prompt = f"MegaGrok comic book style, {prompt}"

    if is_vip:
        return await generate_stability_image(final_prompt)

    return await generate_pollinations_image(final_prompt)

# -----------------------------
# CHAOS FORGE
# -----------------------------
async def generate_chaos_image(is_vip: bool) -> str:
    chaos_scenes = [
        "laughing while reality bends",
        "ruling a meme dimension",
        "breaking the fourth wall",
        "fighting logic itself",
        "emerging from glitching panels",
    ]

    chaos_styles = [
        "absurd comic chaos",
        "psychedelic neon",
        "dramatic cinematic lighting",
        "over-the-top meme energy",
    ]

    prompt = (
        "MegaGrok "
        + random.choice(chaos_scenes)
        + ", "
        + random.choice(chaos_styles)
    )

    if is_vip:
        return await generate_stability_image(prompt)

    return await generate_pollinations_image(prompt)

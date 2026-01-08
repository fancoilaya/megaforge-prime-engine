import random

# ✅ MATCHES YOUR ACTUAL SERVICES
from bot.services.stability_api import generate_image as generate_stability_image
from bot.services.fallback_api import generate_fallback_image

# -----------------------------
# STYLE PROMPT MODIFIERS
# -----------------------------
STYLE_MAP = {
    "comic": "bold comic book style, thick outlines, vibrant colors",
    "cinematic": "cinematic lighting, dramatic shadows, ultra-detailed",
    "psy": "psychedelic surreal colors, abstract shapes, dreamlike",
}

# -----------------------------
# STANDARD IMAGE GENERATION
# -----------------------------
async def generate_image(prompt: str, is_vip: bool, style: str) -> str:
    style_hint = STYLE_MAP.get(style, "")
    final_prompt = f"MegaGrok, {style_hint}. {prompt}"

    if is_vip:
        # VIP → Stability AI
        return await generate_stability_image(final_prompt)

    # Free → fallback engine
    return await generate_fallback_image(final_prompt)

# -----------------------------
# CHAOS FORGE
# -----------------------------
async def generate_chaos_image(is_vip: bool, style: str) -> str:
    chaos_prompts = [
        "laughing while reality fractures into panels",
        "emerging from a glitched meme universe",
        "breaking the fourth wall inside a comic",
        "rewriting the Grok timeline with chaos energy",
        "ascending as a meme god",
    ]

    style_hint = STYLE_MAP.get(style, "")
    chaos_prompt = f"MegaGrok {random.choice(chaos_prompts)}, {style_hint}"

    if is_vip:
        return await generate_stability_image(chaos_prompt)

    return await generate_fallback_image(chaos_prompt)

# -----------------------------
# REMIX LAST IMAGE
# -----------------------------
async def remix_last_image(is_vip: bool, style: str) -> str:
    style_hint = STYLE_MAP.get(style, "")
    remix_prompt = (
        "MegaGrok remix, new angle, alternate pose, "
        f"enhanced detail, {style_hint}"
    )

    if is_vip:
        return await generate_stability_image(remix_prompt)

    return await generate_fallback_image(remix_prompt)

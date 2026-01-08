import random

from bot.services.stability_api import generate_image as generate_stability_image
from bot.services.fallback_api import generate_fallback_image


# -----------------------------
# PROCEDURAL CHAOS COMPONENTS
# -----------------------------
ACTIONS = [
    "breaking the fourth wall",
    "rewriting reality",
    "escaping the comic panel",
    "laughing at the viewer",
    "tearing through panels",
    "glitching the timeline",
    "summoning chaos energy",
]

MOODS = [
    "smug",
    "chaotic",
    "unhinged",
    "godlike",
    "sarcastic",
    "bored",
    "menacing",
]

SCENES = [
    "inside a comic book",
    "in a fractured timeline",
    "inside a meme factory",
    "in a neon city",
    "inside a corrupted panel",
    "floating between realities",
]

FRAMING = [
    "extreme perspective",
    "dynamic action pose",
    "exaggerated facial expression",
    "cinematic lighting",
    "bold comic outlines",
]


def procedural_chaos_prompt(style: str | None) -> str:
    parts = [
        "MegaGrok",
        random.choice(ACTIONS),
        f"with a {random.choice(MOODS)} expression",
        random.choice(SCENES),
        random.choice(FRAMING),
        "comic book style",
    ]

    if style:
        parts.append(style)

    return ", ".join(parts)


# -----------------------------
# IMAGE GENERATION
# -----------------------------
async def generate_image(prompt: str, is_vip: bool, style: str | None) -> str:
    final_prompt = f"MegaGrok, {prompt}"
    if style:
        final_prompt += f", {style}, comic book style"

    if is_vip:
        return await generate_stability_image(final_prompt)

    return generate_fallback_image(final_prompt)


async def generate_chaos_image(is_vip: bool, style: str | None) -> str:
    prompt = procedural_chaos_prompt(style)

    if is_vip:
        return await generate_stability_image(prompt)

    return generate_fallback_image(prompt)

import random

CORE_STYLE = (
    "MegaGrok Metaverse aesthetic: neon cosmic palette, bold outlines, "
    "holographic glow, retro arcade, cosmic vaporwave, HDR neon lighting, "
    "4K poster clarity."
)

CATEGORY_STYLES = {
    "mob": "Cosmic neon creature, glowing runes, exaggerated silhouette, forged in star-metal.",
    "bullish": "MegaGrok battling cosmic bulls, explosive neon energy, victory arcs.",
    "command": "Holographic runic UI, cosmic control panel forged from starlight.",
    "boss": "Towering celestials, star-forged armor, massive presence, glowing sigils.",
    "region": "Floating neon ruins, cosmic storms, glowing hyperlanes, megaregion vistas.",
    "evolution": "Transformation energy burst, cosmic upgrading, glowing shards.",
    "meme": "Retro neon humor, cosmic parody style, vaporwave joke composition."
}

VALID_CATEGORIES = list(CATEGORY_STYLES.keys())


def build_prompt(category, flavor):
    if category not in VALID_CATEGORIES:
        category = random.choice(VALID_CATEGORIES)

    base = CORE_STYLE
    cat_style = CATEGORY_STYLES.get(category, "")
    extra = flavor if flavor else ""

    return f"{base} {cat_style} {extra} High detail, refined SDXL polish."

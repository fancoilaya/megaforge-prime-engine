from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(vip: dict, remaining: int | None):
    """
    Main MegaForge menu.
    vip: dict with at least {"is_vip": bool}
    remaining: cooldown seconds remaining or None
    """

    is_vip = vip.get("is_vip", False)

    cooldown_text = (
        f"⏳ Image cooldown: {remaining // 60}m {remaining % 60}s"
        if remaining and remaining > 0
        else "✅ Image forge ready"
    )

    vip_text = "🟢 VIP ACTIVE" if is_vip else "🔴 FREE USER"

    keyboard = [
        [
            InlineKeyboardButton("🎨 Image Forge", callback_data="forge_image"),
        ],
        [
            InlineKeyboardButton("🎲 Surprise Me", callback_data="forge_surprise"),
        ],
        [
            InlineKeyboardButton(
                "🖼 Meme Forge (VIP)",
                callback_data="forge_meme" if is_vip else "vip_required",
            ),
        ],
        [
            InlineKeyboardButton(
                "🧩 Sticker Forge (VIP)",
                callback_data="forge_sticker" if is_vip else "vip_required",
            ),
        ],
        [
            InlineKeyboardButton(
                "💎 Open VIP Bot",
                url="https://t.me/MegaGrokVIPBot",
            )
        ],
    ]

    header = f"🔥 MegaForge\n{vip_text}\n{cooldown_text}"

    return InlineKeyboardMarkup(keyboard), header

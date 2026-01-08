from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# IMPORTANT:
# This should be the Telegram username of your VIP bot
VIP_BOT_URL = "https://t.me/MegaGrokVIPBot"


def main_menu(is_vip: bool):
    rows = [
        [InlineKeyboardButton("🖼 Image Forge", callback_data="mf_image")],
        [InlineKeyboardButton("😈 Meme Forge 🔒", callback_data="mf_meme")],
        [InlineKeyboardButton("🧩 Sticker Forge 🔒", callback_data="mf_sticker")],
        [InlineKeyboardButton("🎛 Presets 🔒", callback_data="mf_presets")],
    ]

    if not is_vip:
        rows.append([
            InlineKeyboardButton(
                "🔗 Link Wallet (Enable VIP)",
                url=f"{VIP_BOT_URL}?start=link"
            )
        ])

    rows.append([InlineKeyboardButton("❌ Exit", callback_data="mf_exit")])

    return InlineKeyboardMarkup(rows)


def vip_locked_message() -> str:
    return (
        "🔒 **VIP FORGE LOCKED**\n\n"
        "This forge requires **VIP access**.\n\n"
        "✨ VIP unlocks:\n"
        "• High-quality image rendering\n"
        "• Faster cooldowns\n"
        "• Meme & Sticker Forge\n"
        "• Presets & future tools\n\n"
        "🔐 **Wallet linking is handled securely** via the\n"
        "**MegaGrok VIP Bot** in a private chat.\n\n"
        "👇 Enable VIP below"
    )


def vip_locked_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔗 Open VIP Bot (Link Wallet)",
                url=f"{VIP_BOT_URL}?start=link"
            )
        ],
        [
            InlineKeyboardButton("⬅ Back to Forge", callback_data="mf_back")
        ]
    ])

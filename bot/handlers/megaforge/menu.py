from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import VIP_SERVICE_URL

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
                url=f"{VIP_SERVICE_URL}/link"
            )
        ])

    rows.append([InlineKeyboardButton("❌ Exit", callback_data="mf_exit")])

    return InlineKeyboardMarkup(rows)

def vip_locked_message() -> str:
    return (
        "🔒 **VIP FORGE LOCKED**\n\n"
        "This forge requires VIP access.\n\n"
        "VIP unlocks:\n"
        "• High-quality image rendering\n"
        "• Faster cooldowns\n"
        "• Meme & Sticker Forge\n"
        "• Presets & future tools\n\n"
        "👇 Enable VIP below"
    )

def vip_locked_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔗 Link Wallet (Enable VIP)",
                url=f"{VIP_SERVICE_URL}/link"
            )
        ],
        [
            InlineKeyboardButton("⬅ Back to Forge", callback_data="mf_back")
        ]
    ])

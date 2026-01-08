from telegram import InlineKeyboardButton, InlineKeyboardMarkup


VIP_BOT_URL = "https://t.me/MegaGrokVIPBot"  # change if needed


def main_menu(vip: bool):
    buttons = [
        [InlineKeyboardButton("🖼 Image Forge", callback_data="image_forge")],
        [InlineKeyboardButton("🎲 Surprise Me", callback_data="surprise_me")],
    ]

    if vip:
        buttons.append([InlineKeyboardButton("😈 Meme Forge", callback_data="meme_forge")])
        buttons.append([InlineKeyboardButton("🧩 Sticker Forge", callback_data="sticker_forge")])
    else:
        buttons.append([InlineKeyboardButton("😈 Meme Forge 🔒 VIP", callback_data="vip_required")])
        buttons.append([InlineKeyboardButton("🧩 Sticker Forge 🔒 VIP", callback_data="vip_required")])

    # VIP BOT LINK (always visible)
    buttons.append([
        InlineKeyboardButton(
            "🔗 Link Wallet (VIP Bot)",
            url=VIP_BOT_URL
        )
    ])

    buttons.append([InlineKeyboardButton("❌ Exit", callback_data="exit")])

    return InlineKeyboardMarkup(buttons)

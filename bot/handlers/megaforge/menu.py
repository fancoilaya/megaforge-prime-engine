from telegram import InlineKeyboardMarkup, InlineKeyboardButton

VIP_BOT_URL = "https://t.me/MegaGrokVIPBot"

# -----------------------------
# MAIN MENU
# -----------------------------
def main_menu(is_vip: bool):
    rows = [
        [InlineKeyboardButton("🖼 Image Forge", callback_data="mf_image_menu")],
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

# -----------------------------
# IMAGE FORGE SUB MENU
# -----------------------------
def image_forge_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Free Prompt", callback_data="if_free")],
        [InlineKeyboardButton("🎭 Chaos Forge", callback_data="if_chaos")],
        [InlineKeyboardButton("⬅ Back", callback_data="mf_back")],
    ])

# -----------------------------
# VIP LOCKED
# -----------------------------
def vip_locked_message():
    return (
        "🔒 **VIP FORGE LOCKED**\n\n"
        "This forge requires **VIP access**.\n\n"
        "🔐 Wallet linking is handled securely via the\n"
        "**MegaGrok VIP Bot** in private chat."
    )

def vip_locked_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔗 Open VIP Bot",
                url=f"{VIP_BOT_URL}?start=link"
            )
        ],
        [InlineKeyboardButton("⬅ Back", callback_data="mf_back")]
    ])

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Telegram username of the VIP bot
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
# IMAGE FORGE SUB-MENU
# -----------------------------
def image_forge_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Free Prompt", callback_data="if_free")],
        [InlineKeyboardButton("🎭 Chaos Forge", callback_data="if_chaos")],
        [InlineKeyboardButton("🎨 Style Picker", callback_data="if_style")],
        [InlineKeyboardButton("⬅ Back", callback_data="mf_back")],
    ])

# -----------------------------
# STYLE PICKER MENU
# -----------------------------
def style_picker_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖊 Comic Classic", callback_data="style_comic")],
        [InlineKeyboardButton("🎞 Cinematic", callback_data="style_cinematic")],
        [InlineKeyboardButton("🤯 Psychedelic", callback_data="style_psy")],
        [InlineKeyboardButton("⬅ Back", callback_data="mf_image_menu")],
    ])

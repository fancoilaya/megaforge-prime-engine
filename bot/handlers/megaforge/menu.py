from telegram import InlineKeyboardMarkup, InlineKeyboardButton

VIP_BOT_URL = "https://t.me/MegaGrokVIPBot"


def main_menu(is_vip: bool):
    rows = [
        [InlineKeyboardButton("🖼 Image Forge", callback_data="mf_image_menu")],
        [InlineKeyboardButton("❌ Exit", callback_data="mf_exit")],
    ]

    if not is_vip:
        rows.insert(
            1,
            [InlineKeyboardButton("🔗 Link Wallet (Enable VIP)", url=f"{VIP_BOT_URL}?start=link")]
        )

    return InlineKeyboardMarkup(rows)


def image_forge_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Free Prompt", callback_data="if_free")],
        [InlineKeyboardButton("🎲 Surprise Me", callback_data="if_chaos")],
        [InlineKeyboardButton("🎨 Style Picker", callback_data="if_style")],
        [InlineKeyboardButton("⬅ Back", callback_data="mf_back")],
    ])


def style_picker_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖊 Comic Classic", callback_data="style_comic")],
        [InlineKeyboardButton("🎞 Cinematic", callback_data="style_cinematic")],
        [InlineKeyboardButton("🤯 Psychedelic", callback_data="style_psy")],
        [InlineKeyboardButton("⬅ Back", callback_data="mf_image_menu")],
    ])

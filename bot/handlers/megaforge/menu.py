from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(is_vip: bool):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Image Forge", callback_data="mf_image")],
        [InlineKeyboardButton("😈 Meme Forge 🔒", callback_data="mf_meme")],
        [InlineKeyboardButton("🧩 Sticker Forge 🔒", callback_data="mf_sticker")],
        [InlineKeyboardButton("🎛 Presets 🔒", callback_data="mf_presets")],
        [InlineKeyboardButton("❌ Exit", callback_data="mf_exit")],
    ])

def vip_locked_message() -> str:
    return (
        "🔒 **VIP FORGE LOCKED**\n\n"
        "This forge requires VIP access.\n\n"
        "VIP unlocks:\n"
        "• High-quality image rendering\n"
        "• Faster cooldowns\n"
        "• Meme & Sticker Forge\n"
        "• Presets & future tools\n\n"
        "[ 🔗 Link Wallet to Enable VIP ]"
    )

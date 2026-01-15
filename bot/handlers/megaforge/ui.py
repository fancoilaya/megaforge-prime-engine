from telegram import Update
from telegram.ext import ContextTypes

from .menu import main_menu
from .cooldowns import image_cooldown_remaining, mark_image_used
from .vip import get_vip_status
from .generators import generate_image


# ---------------------------------------------------------
# /megaforge ENTRY
# ---------------------------------------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    vip = get_vip_status(user.id)
    remaining = image_cooldown_remaining(user.id, vip["is_vip"])

    keyboard, header = main_menu(vip, remaining)

    intro = (
        "🔥 **MEGAFORGE**\n\n"
        "MegaForge is the creative engine of **MegaGrok**.\n"
        "Here you forge comic-style art, surreal scenes, memes, "
        "and visual experiments powered by Grok.\n\n"
        "Every image is generated live — no templates, no repeats.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👤 **Your Status**\n"
    )

    await update.message.reply_text(
        intro + header,
        reply_markup=keyboard,
    )


# ---------------------------------------------------------
# CALLBACK HANDLER
# ---------------------------------------------------------

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    vip = get_vip_status(user.id)
    remaining = image_cooldown_remaining(user.id, vip["is_vip"])

    data = query.data

    # BLOCK ALL IMAGE ACTIONS ON COOLDOWN
    if remaining and remaining > 0 and data.startswith("forge_"):
        keyboard, header = main_menu(vip, remaining)
        await query.edit_message_text(
            "⏳ **Image Forge on Cooldown**\n\n"
            "You’ve recently forged an image.\n"
            "Please wait before forging again.\n\n"
            + header,
            reply_markup=keyboard,
        )
        return

    # IMAGE FORGE (USER PROMPT)
    if data == "forge_image":
        context.user_data["awaiting_prompt"] = True
        await query.edit_message_text(
            "✍️ **Image Forge**\n\n"
            "Send a prompt describing what you want to see.\n\n"
            "Tips:\n"
            "• Characters, actions, emotions\n"
            "• Comic or cinematic moments\n"
            "• MegaGrok themes welcome\n\n"
            "_Your prompt is used once for this image only._"
        )
        return

    # SURPRISE ME (PROCEDURAL PROMPT)
    if data == "forge_surprise":
        await query.edit_message_text(
            "🎲 **Surprise Forge**\n\n"
            "MegaGrok is improvising something unexpected...\n"
            "Forging image now ⏳"
        )

        prompt = (
            "MegaGrok in a dramatic comic-book scene, "
            "bold ink lines, dynamic pose, expressive emotion, "
            "high contrast, graphic novel style"
        )

        path = await generate_image(prompt, vip["is_vip"])
        mark_image_used(user.id)

        await query.message.reply_photo(photo=path)
        return

    # VIP LOCK
    if data == "vip_required":
        await query.edit_message_text(
            "🔒 **VIP Feature**\n\n"
            "This forge mode is reserved for VIP holders.\n\n"
            "VIP unlocks:\n"
            "• Faster cooldowns\n"
            "• Meme & Sticker Forge\n"
            "• Higher-tier generation\n\n"
            "🔗 Link your wallet securely via the VIP bot:\n"
            "👉 https://t.me/MegaGrokVIPBot"
        )
        return


# ---------------------------------------------------------
# TEXT PROMPT HANDLER
# ---------------------------------------------------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_prompt"):
        return

    user = update.effective_user
    vip = get_vip_status(user.id)
    remaining = image_cooldown_remaining(user.id, vip["is_vip"])

    if remaining and remaining > 0:
        await update.message.reply_text(
            "⏳ Image Forge is still cooling down.\n"
            "Please wait before sending another prompt."
        )
        return

    prompt = update.message.text
    context.user_data["awaiting_prompt"] = False

    forge_mode = (
        "🟢 **VIP Forge Active — High Quality Enabled**"
        if vip["is_vip"]
        else "🔴 **Free Forge Active**"
    )
    
    await update.message.reply_text(
        "🎨 **Forge in Progress**\n\n"
        "MegaGrok is rendering your idea...\n"
        "This can take a moment ⏳"
    )

    path = await generate_image(prompt, vip["is_vip"])
    mark_image_used(user.id)

    await update.message.reply_photo(photo=path)

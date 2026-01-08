from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from .menu import main_menu
from .cooldowns import image_cooldown_remaining, mark_image_used
from .vip import get_vip_status
from .generators import generate_image, generate_surprise_image


# ---------------------------------------------------------
# ENTRY POINT: /megaforge
# ---------------------------------------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    vip = get_vip_status(user.id)
    remaining = image_cooldown_remaining(user.id, vip["is_vip"])

    keyboard, header = main_menu(vip, remaining)

    await update.message.reply_text(
        header,
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

    # Cooldown active → block ALL image actions
    if remaining and remaining > 0 and data.startswith("forge_"):
        keyboard, header = main_menu(vip, remaining)
        await query.edit_message_text(
            f"⛔ Image forging is on cooldown.\n\n{header}",
            reply_markup=keyboard,
        )
        return

    # -------------------------------------------------
    # IMAGE FORGE (TEXT INPUT)
    # -------------------------------------------------
    if data == "forge_image":
        context.user_data["awaiting_prompt"] = True
        await query.edit_message_text(
            "✍️ Type your image prompt.\n\n"
            "MegaGrok will interpret it in comic-book style."
        )
        return

    # -------------------------------------------------
    # SURPRISE ME
    # -------------------------------------------------
    if data == "forge_surprise":
        await query.edit_message_text("🎲 Forging a surprise MegaGrok image…")

        path = await generate_surprise_image(vip["is_vip"])
        mark_image_used(user.id)

        await query.message.reply_photo(photo=path)
        return

    # -------------------------------------------------
    # VIP LOCKED FEATURES
    # -------------------------------------------------
    if data == "vip_required":
        await query.edit_message_text(
            "🔒 This feature is VIP-only.\n\n"
            "Open the VIP bot to unlock MegaForge powers:\n"
            "👉 https://t.me/MegaGrokVIPBot"
        )
        return


# ---------------------------------------------------------
# TEXT INPUT HANDLER (PROMPT)
# ---------------------------------------------------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_prompt"):
        return

    user = update.effective_user
    vip = get_vip_status(user.id)
    remaining = image_cooldown_remaining(user.id, vip["is_vip"])

    if remaining and remaining > 0:
        await update.message.reply_text("⛔ Image forging is currently on cooldown.")
        return

    prompt = update.message.text
    context.user_data["awaiting_prompt"] = False

    await update.message.reply_text("🎨 Forging your MegaGrok image…")

    path = await generate_image(prompt, vip["is_vip"])
    mark_image_used(user.id)

    await update.message.reply_photo(photo=path)

import logging
import time
from telegram import Update
from telegram.ext import ContextTypes

from .sessions import get_session, ForgeState
from .vip import check_vip_status
from .cooldowns import image_cooldown_remaining
from .menu import main_menu, vip_locked_message
from .generators import generate_image_for_session

logging.info("📦 Loading MegaForge UI module")

async def safe_reply(source, text, **kwargs):
    try:
        if hasattr(source, "edit_message_text"):
            await source.edit_message_text(text, **kwargs)
        else:
            await source.message.reply_text(text, **kwargs)
    except Exception:
        await source.message.reply_text(text, **kwargs)

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)
    session["last_used"] = int(time.time())

    session["is_vip"] = check_vip_status(user_id)
    session["engine"] = "vip" if session["is_vip"] else "free"
    session["state"] = ForgeState.MAIN_MENU

    status_block = (
        "━━━━━━━━━━━━━━━━━━\n"
        "👤 **Your Status**\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if session['is_vip'] else '🔴 NOT ENABLED'}\n"
        f"Image Forge: {'✨ High Quality' if session['is_vip'] else '🟢 Standard Quality'}\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    await update.message.reply_text(
        "🔥 **MEGAFORGE**\n\n"
        "The MegaForge is a creative engine powered by MegaGrok.\n"
        "Here you forge comic-style art, memes, stickers, and viral content —\n"
        "all centered around the Grok universe.\n\n"
        f"{status_block}\n\n"
        "Choose a forge mode:",
        reply_markup=main_menu(session["is_vip"]),
        parse_mode="Markdown"
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = get_session(user_id)
    session["last_used"] = int(time.time())

    if query.data == "mf_exit":
        session["state"] = ForgeState.EXIT
        await safe_reply(query, "🧱 MegaForge closed.")
        return

    if query.data == "mf_image":
        session["state"] = ForgeState.IMAGE_INPUT
        await safe_reply(
            query,
            "🖼 **IMAGE FORGE**\n\n"
            "Describe what MegaGrok is doing.\n"
            "Comic book style is always applied.",
            parse_mode="Markdown"
        )
        return

    if query.data in ("mf_meme", "mf_sticker", "mf_presets"):
        if not session["is_vip"]:
            await safe_reply(query, vip_locked_message(), parse_mode="Markdown")
            return

        await safe_reply(query, "✨ VIP forge coming online soon.")
        return

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)
    session["last_used"] = int(time.time())

    if session["state"] != ForgeState.IMAGE_INPUT:
        return

    prompt = update.message.text.strip()
    await run_image_generation(update, session, prompt)

async def run_image_generation(source, session: dict, prompt: str):
    remaining = image_cooldown_remaining(session)
    if remaining > 0:
        await safe_reply(source, f"⏳ Cooldown active: {remaining}s remaining")
        return

    await safe_reply(source, "🧨 Forging image...")

    image_path = await generate_image_for_session(
        f"MegaGrok comic book style. {prompt}",
        session["is_vip"],
    )

    session["cooldowns"]["image"] = int(time.time())
    session["state"] = ForgeState.MAIN_MENU

    with open(image_path, "rb") as img:
        await source.message.reply_photo(
            photo=img,
            reply_markup=main_menu(session["is_vip"])
        )

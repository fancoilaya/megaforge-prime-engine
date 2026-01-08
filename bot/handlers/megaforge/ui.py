import time
from telegram import Update
from telegram.ext import ContextTypes

from .sessions import get_session, ForgeState
from .vip import fetch_vip_status
from .cooldowns import image_cooldown_remaining
from .menu import main_menu, image_forge_menu, vip_locked_message, vip_locked_keyboard
from .generators import generate_image, generate_chaos_image

# -----------------------------
async def safe_reply(source, text, **kwargs):
    try:
        if hasattr(source, "edit_message_text"):
            await source.edit_message_text(text, **kwargs)
        else:
            await source.message.reply_text(text, **kwargs)
    except Exception:
        await source.message.reply_text(text, **kwargs)

# -----------------------------
# /megaforge
# -----------------------------
async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = get_session(user.id)

    vip = fetch_vip_status(user.id)
    session["vip"] = vip
    session["state"] = ForgeState.MAIN_MENU

    await update.message.reply_text(
        "🔥 **MEGAFORGE**\n\n"
        "Forge comic-style art, memes & chaos.\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if vip['is_vip'] else '🔴 NOT ENABLED'}\n\n"
        "Choose a forge mode:",
        reply_markup=main_menu(vip["is_vip"]),
        parse_mode="Markdown"
    )

# -----------------------------
# CALLBACKS
# -----------------------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    session = get_session(query.from_user.id)
    vip = session["vip"]

    # MAIN NAV
    if query.data == "mf_exit":
        await safe_reply(query, "❌ MegaForge closed.")
        return

    if query.data == "mf_back":
        await safe_reply(query, "🔙 Back to MegaForge", reply_markup=main_menu(vip["is_vip"]))
        return

    # IMAGE FORGE MENU
    if query.data == "mf_image_menu":
        await safe_reply(
            query,
            "🖼 **IMAGE FORGE**\n\nChoose how you want to forge:",
            reply_markup=image_forge_menu(),
            parse_mode="Markdown",
        )
        return

    # FREE PROMPT
    if query.data == "if_free":
        session["state"] = ForgeState.IMAGE_INPUT
        session["image_mode"] = "free"
        await safe_reply(query, "✍️ Describe what MegaGrok is doing:")
        return

    # CHAOS FORGE
    if query.data == "if_chaos":
        remaining = image_cooldown_remaining(session)
        if remaining > 0:
            await safe_reply(query, f"⏳ Cooldown: {remaining}s")
            return

        await safe_reply(query, "🎭 **Chaos unleashed…**")
        image_path = await generate_chaos_image(vip["is_vip"])
        session["cooldowns"]["image"] = int(time.time())

        with open(image_path, "rb") as img:
            await query.message.reply_photo(
                photo=img,
                reply_markup=main_menu(vip["is_vip"])
            )
        return

# -----------------------------
# TEXT INPUT
# -----------------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = get_session(update.effective_user.id)

    if session.get("state") != ForgeState.IMAGE_INPUT:
        return

    vip = session["vip"]
    remaining = image_cooldown_remaining(session)

    if remaining > 0:
        await update.message.reply_text(f"⏳ Cooldown: {remaining}s")
        return

    image_path = await generate_image(update.message.text, vip["is_vip"])
    session["cooldowns"]["image"] = int(time.time())
    session["state"] = ForgeState.MAIN_MENU

    with open(image_path, "rb") as img:
        await update.message.reply_photo(
            photo=img,
            reply_markup=main_menu(vip["is_vip"])
        )

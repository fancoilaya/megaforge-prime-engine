import time
from telegram import Update
from telegram.ext import ContextTypes

from .sessions import get_session, ForgeState
from .vip import fetch_vip_status
from .cooldowns import image_cooldown_remaining
from .menu import main_menu, image_forge_menu, style_picker_menu
from .generators import generate_image, generate_chaos_image


# -----------------------------
# /megaforge ENTRY
# -----------------------------
async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = get_session(user.id)

    vip = fetch_vip_status(user.id)
    session["vip"] = vip
    session["state"] = ForgeState.MAIN_MENU
    session.setdefault("style", None)

    await update.message.reply_text(
        "🔥 **MEGAFORGE**\n\n"
        "Create comic-style MegaGrok art.\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if vip['is_vip'] else '🔴 NOT ENABLED'}",
        reply_markup=main_menu(vip["is_vip"]),
        parse_mode="Markdown",
    )


# -----------------------------
# CALLBACK HANDLER
# -----------------------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = get_session(user_id)

    # 🔒 SAFE VIP INITIALIZATION (FIX)
    vip = session.get("vip")
    if not vip:
        vip = fetch_vip_status(user_id)
        session["vip"] = vip

    style = session.get("style")

    # EXIT
    if query.data == "mf_exit":
        await query.edit_message_text("❌ MegaForge closed.")
        return

    # BACK
    if query.data == "mf_back":
        await query.edit_message_text(
            "🔙 MegaForge",
            reply_markup=main_menu(vip["is_vip"]),
        )
        return

    # IMAGE FORGE MENU
    if query.data == "mf_image_menu":
        await query.edit_message_text(
            "🖼 **IMAGE FORGE**\n\n"
            "Type a prompt or try 🎲 Surprise Me:",
            reply_markup=image_forge_menu(),
            parse_mode="Markdown",
        )
        return

    # FREE PROMPT
    if query.data == "if_free":
        session["state"] = ForgeState.IMAGE_INPUT
        await query.edit_message_text("✍️ Describe what MegaGrok is doing:")
        return

    # CHAOS / SURPRISE ME
    if query.data == "if_chaos":
        if image_cooldown_remaining(session) > 0:
            await query.edit_message_text("⏳ Image Forge cooling down.")
            return

        await query.edit_message_text("🎲 **Surprise Me activated…**", parse_mode="Markdown")
        path = await generate_chaos_image(vip["is_vip"], style)
        session["cooldowns"]["image"] = int(time.time())

        with open(path, "rb") as img:
            await query.message.reply_photo(
                img,
                reply_markup=main_menu(vip["is_vip"])
            )
        return

    # STYLE PICKER
    if query.data == "if_style":
        await query.edit_message_text(
            "🎨 Choose a style (applies to next images):",
            reply_markup=style_picker_menu(),
        )
        return

    if query.data.startswith("style_"):
        session["style"] = query.data.replace("style_", "")
        await query.edit_message_text(f"✅ Style set: {session['style'].title()}")
        return


# -----------------------------
# TEXT INPUT HANDLER
# -----------------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if session.get("state") != ForgeState.IMAGE_INPUT:
        return

    vip = session.get("vip")
    if not vip:
        vip = fetch_vip_status(user_id)
        session["vip"] = vip

    style = session.get("style")

    if image_cooldown_remaining(session) > 0:
        await update.message.reply_text("⏳ Image Forge cooling down.")
        return

    path = await generate_image(update.message.text, vip["is_vip"], style)
    session["cooldowns"]["image"] = int(time.time())
    session["state"] = ForgeState.MAIN_MENU

    with open(path, "rb") as img:
        await update.message.reply_photo(
            img,
            reply_markup=main_menu(vip["is_vip"])
        )

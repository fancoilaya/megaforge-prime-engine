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
    user_id = update.effective_user.id
    session = get_session(user_id)

    vip = fetch_vip_status(user_id)
    session.clear()  # 🔥 RESET SESSION EVERY RUN
    session["vip"] = vip
    session["state"] = ForgeState.MAIN_MENU
    session["style"] = None

    await update.message.reply_text(
        "🔥 **MEGAFORGE**\n\n"
        "Create comic-style MegaGrok art.\n\n"
        "• ✍️ Write what MegaGrok is doing\n"
        "• 🎲 Or let MegaForge surprise you\n"
        "• 🎨 Optional style picker\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if vip['is_vip'] else '🔴 NOT ENABLED'}",
        reply_markup=image_forge_menu(),
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

    vip = session.get("vip") or fetch_vip_status(user_id)
    session["vip"] = vip
    style = session.get("style")

    # STYLE PICKER
    if query.data == "if_style":
        await query.message.reply_text(
            "🎨 Choose a style (applies to the next image only):",
            reply_markup=style_picker_menu(),
        )
        return

    if query.data.startswith("style_"):
        session["style"] = query.data.replace("style_", "")
        await query.message.reply_text(
            f"✅ Style set: **{session['style'].title()}**\n\n"
            "Now generate an image.",
            parse_mode="Markdown",
        )
        return

    # FREE PROMPT
    if query.data == "if_free":
        session["state"] = ForgeState.IMAGE_INPUT
        await query.message.reply_text("✍️ Describe what **MegaGrok** is doing:")
        return

    # SURPRISE ME (PROCEDURAL CHAOS)
    if query.data == "if_chaos":
        if image_cooldown_remaining(session) > 0:
            await query.message.reply_text("⏳ Image Forge cooling down.")
            return

        await query.message.reply_text("🎲 **Forging chaotic MegaGrok comic…**", parse_mode="Markdown")

        path = await generate_chaos_image(
            vip["is_vip"],
            session.get("style"),
        )

        session["cooldowns"]["image"] = int(time.time())
        session.clear()  # 🔥 END SESSION AFTER IMAGE

        with open(path, "rb") as img:
            await query.message.reply_photo(img)

        await query.message.reply_text(
            "🖼 **MegaForge complete.**\n\n"
            "Run `/megaforge` to forge another image.",
            parse_mode="Markdown",
        )
        return


# -----------------------------
# TEXT INPUT HANDLER
# -----------------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if session.get("state") != ForgeState.IMAGE_INPUT:
        return

    vip = session.get("vip") or fetch_vip_status(user_id)
    session["vip"] = vip

    if image_cooldown_remaining(session) > 0:
        await update.message.reply_text("⏳ Image Forge cooling down.")
        return

    style = session.get("style")

    # HARD ANCHOR MEGAGROK + COMIC
    prompt = (
        f"MegaGrok comic character, {update.message.text}, "
        "comic book style, bold outlines, expressive character"
    )

    if style:
        prompt += f", {style}"

    path = await generate_image(prompt, vip["is_vip"], style)

    session["cooldowns"]["image"] = int(time.time())
    session.clear()  # 🔥 END SESSION AFTER IMAGE

    with open(path, "rb") as img:
        await update.message.reply_photo(img)

    await update.message.reply_text(
        "🖼 **MegaForge complete.**\n\n"
        "Run `/megaforge` to forge another image.",
        parse_mode="Markdown",
    )

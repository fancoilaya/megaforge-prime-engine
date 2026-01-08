import time
from telegram import Update
from telegram.ext import ContextTypes

from .sessions import get_session, ForgeState
from .vip import fetch_vip_status
from .cooldowns import image_cooldown_remaining
from .menu import main_menu
from .generators import generate_image, generate_chaos_image


def _cooldown_text(session, vip):
    remaining = image_cooldown_remaining(session)

    if remaining <= 0:
        return "✅ Image Forge Ready"

    minutes = remaining // 60
    if vip["is_vip"]:
        return f"⚡ VIP Cooldown: {minutes}m remaining"
    return f"⏱ Image Cooldown: {minutes}m remaining"


# -----------------------------
# /megaforge ENTRY
# -----------------------------
async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    vip = fetch_vip_status(user_id)

    session.clear()
    session["vip"] = vip
    session["state"] = ForgeState.MAIN_MENU

    cooldown_status = _cooldown_text(session, vip)

    await update.message.reply_text(
        "🔥 **MEGAFORGE**\n\n"
        "Forge comic-style art, memes & stickers\n"
        "powered by **MegaGrok**.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👤 **Your Status**\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if vip['is_vip'] else '🔴 NOT ENABLED'}\n"
        f"{cooldown_status}\n\n"
        "💡 Wallet linking is handled **securely** via the MegaGrok VIP Bot.\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Choose a forge mode:",
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
    vip = session.get("vip") or fetch_vip_status(user_id)
    session["vip"] = vip

    # EXIT
    if query.data == "exit":
        session.clear()
        await query.message.reply_text("👋 MegaForge closed.")
        return

    # VIP LOCK
    if query.data == "vip_required":
        await query.message.reply_text(
            "🔒 This forge is VIP-only.\n\n"
            "Use the **Link Wallet (VIP Bot)** button to unlock.",
            parse_mode="Markdown",
        )
        return

    # IMAGE FORGE
    if query.data == "image_forge":
        if image_cooldown_remaining(session) > 0:
            await query.message.reply_text("⏳ Image Forge is cooling down.")
            return

        session["state"] = ForgeState.IMAGE_INPUT
        await query.message.reply_text("✍️ Describe what **MegaGrok** is doing:")
        return

    # SURPRISE ME
    if query.data == "surprise_me":
        if image_cooldown_remaining(session) > 0:
            await query.message.reply_text("⏳ Image Forge is cooling down.")
            return

        await query.message.reply_text(
            "🔥 MegaForge is forging chaos...\n⏳ This may take a moment."
        )

        path = await generate_chaos_image(vip["is_vip"])

        session["cooldowns"]["image"] = int(time.time())
        session.clear()

        with open(path, "rb") as img:
            await query.message.reply_photo(img)

        await query.message.reply_text(
            "🖼 **Forge complete.**\n\nRun `/megaforge` to forge again.",
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
        await update.message.reply_text("⏳ Image Forge is cooling down.")
        return

    await update.message.reply_text(
        "🔥 MegaForge is forging your image...\n⏳ This may take a moment."
    )

    prompt = (
        f"MegaGrok comic character, {update.message.text}, "
        "comic book style, bold outlines, expressive character"
    )

    path = await generate_image(prompt, vip["is_vip"])

    session["cooldowns"]["image"] = int(time.time())
    session.clear()

    with open(path, "rb") as img:
        await update.message.reply_photo(img)

    await update.message.reply_text(
        "🖼 **Forge complete.**\n\nRun `/megaforge` to forge again.",
        parse_mode="Markdown",
    )

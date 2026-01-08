from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from .menu import main_menu
from .cooldowns import image_cooldown_remaining, mark_image_used
from .vip import get_vip_status
from .generators import generate_image, generate_surprise_image


# -------------------------
# Internal helpers
# -------------------------

def _get_session(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> dict:
    if "sessions" not in context.bot_data:
        context.bot_data["sessions"] = {}

    if user_id not in context.bot_data["sessions"]:
        context.bot_data["sessions"][user_id] = {}

    return context.bot_data["sessions"][user_id]


def _cooldown_block(session: dict, vip: dict):
    remaining = image_cooldown_remaining(session, vip)
    if remaining is None:
        return False, None
    return True, remaining


# -------------------------
# Entry point: /megaforge
# -------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = _get_session(context, user.id)

    vip = get_vip_status(user.id)
    session["vip"] = vip
    session.pop("awaiting_prompt", None)

    cooldown_text = ""
    remaining = image_cooldown_remaining(session, vip)
    if remaining:
        cooldown_text = f"\n⏳ Cooldown: {remaining}\n"

    text = (
        "🔥 **MEGAFORGE**\n\n"
        "Forge comic-style art powered by MegaGrok.\n\n"
        "👤 **Your Status**\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if vip['is_vip'] else '🔴 NOT ENABLED'}\n"
        f"{cooldown_text}\n"
        "💡 Wallet linking is handled securely via the VIP bot.\n\n"
        "Choose a forge mode:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu(vip),
        parse_mode="Markdown"
    )


# -------------------------
# Button callbacks
# -------------------------

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    session = _get_session(context, user.id)

    vip = session.get("vip") or get_vip_status(user.id)
    session["vip"] = vip

    data = query.data

    # -------------------------
    # IMAGE FORGE (FREE)
    # -------------------------
    if data == "image_forge":
        blocked, remaining = _cooldown_block(session, vip)
        if blocked:
            await query.answer(
                f"⏳ Image Forge is on cooldown ({remaining}).",
                show_alert=True
            )
            return

        session["awaiting_prompt"] = True
        await query.message.reply_text(
            "✏️ Send a prompt for your MegaGrok image."
        )
        return

    # -------------------------
    # SURPRISE ME (FREE)
    # -------------------------
    if data == "surprise_me":
        blocked, remaining = _cooldown_block(session, vip)
        if blocked:
            await query.answer(
                f"⏳ Image Forge is on cooldown ({remaining}).",
                show_alert=True
            )
            return

        await query.message.reply_text("🎨 Forging something unexpected…")
        path = await generate_surprise_image(vip["is_vip"])

        mark_image_used(session)
        session.pop("awaiting_prompt", None)

        await query.message.reply_photo(
            photo=open(path, "rb"),
            caption="🖼️ Forge complete.\n\nRun /megaforge again."
        )
        return

    # -------------------------
    # VIP-LOCKED MODES
    # -------------------------
    if data in ("meme_forge", "sticker_forge"):
        if not vip["is_vip"]:
            await query.answer(
                "🔒 VIP required. Link your wallet via the VIP bot.",
                show_alert=True
            )
            return

        await query.message.reply_text("🚧 Coming soon for VIPs.")
        return

    # -------------------------
    # EXIT
    # -------------------------
    if data == "exit":
        session.clear()
        await query.message.reply_text("❌ MegaForge closed.")
        return


# -------------------------
# Text input (image prompt)
# -------------------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = _get_session(context, user.id)

    if not session.get("awaiting_prompt"):
        return

    vip = session.get("vip") or get_vip_status(user.id)
    session["vip"] = vip

    blocked, remaining = _cooldown_block(session, vip)
    if blocked:
        await update.message.reply_text(
            f"⏳ Image Forge is on cooldown ({remaining})."
        )
        session.pop("awaiting_prompt", None)
        return

    prompt = update.message.text.strip()
    if not prompt:
        await update.message.reply_text("❗ Please send a valid prompt.")
        return

    await update.message.reply_text("🎨 Forging your MegaGrok image…")

    path = await generate_image(prompt, vip["is_vip"])

    mark_image_used(session)
    session.pop("awaiting_prompt", None)

    await update.message.reply_photo(
        photo=open(path, "rb"),
        caption="🖼️ Forge complete.\n\nRun /megaforge again."
    )

from telegram import Update
from telegram.ext import ContextTypes

from .menu import main_menu
from .cooldowns import image_cooldown_remaining, mark_image_used
from .vip import get_vip_status
from .generators import generate_image


# -------------------------
# Session helpers
# -------------------------

def _get_session(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> dict:
    sessions = context.bot_data.setdefault("sessions", {})
    return sessions.setdefault(user_id, {})


def _cooldown_block(session: dict, vip: dict):
    remaining = image_cooldown_remaining(session, vip)
    if remaining:
        return True, remaining
    return False, None


# -------------------------
# /megaforge entry
# -------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = _get_session(context, user.id)

    vip = get_vip_status(user.id)
    session["vip"] = vip
    session.pop("awaiting_prompt", None)

    cooldown = image_cooldown_remaining(session, vip)
    cooldown_text = f"\n⏳ Cooldown: {cooldown}\n" if cooldown else "\n✅ Image Forge Ready\n"

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

    blocked, remaining = _cooldown_block(session, vip)

    if query.data == "image_forge":
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

    if query.data == "surprise_me":
        if blocked:
            await query.answer(
                f"⏳ Image Forge is on cooldown ({remaining}).",
                show_alert=True
            )
            return

        await query.message.reply_text("🎨 Forging something unexpected…")

        # Procedural surprise prompt
        prompt = (
            "MegaGrok comic-style illustration, bold lines, dramatic lighting, "
            "dynamic pose, explosive energy, graphic novel art"
        )

        path = await generate_image(prompt, vip["is_vip"])
        mark_image_used(session)
        session.clear()

        await query.message.reply_photo(
            photo=open(path, "rb"),
            caption="🖼️ Forge complete.\n\nRun /megaforge again."
        )
        return

    if query.data in ("meme_forge", "sticker_forge"):
        if not vip["is_vip"]:
            await query.answer(
                "🔒 VIP required. Link your wallet via the VIP bot.",
                show_alert=True
            )
            return

        await query.message.reply_text("🚧 VIP Forge coming soon.")
        return

    if query.data == "exit":
        session.clear()
        await query.message.reply_text("❌ MegaForge closed.")
        return


# -------------------------
# Prompt handler
# -------------------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = _get_session(context, user.id)

    if not session.get("awaiting_prompt"):
        return

    vip = session.get("vip") or get_vip_status(user.id)
    blocked, remaining = _cooldown_block(session, vip)

    if blocked:
        await update.message.reply_text(
            f"⏳ Image Forge is on cooldown ({remaining})."
        )
        session.clear()
        return

    prompt = update.message.text.strip()
    if not prompt:
        await update.message.reply_text("❗ Please send a valid prompt.")
        return

    await update.message.reply_text("🎨 Forging your MegaGrok image…")

    path = await generate_image(prompt, vip["is_vip"])
    mark_image_used(session)
    session.clear()

    await update.message.reply_photo(
        photo=open(path, "rb"),
        caption="🖼️ Forge complete.\n\nRun /megaforge again."
    )

import time
from telegram import Update
from telegram.ext import ContextTypes

from .menu import main_menu
from .generators import generate_image
from .cooldowns import image_cooldown_remaining, mark_image_used
from .sessions import get_session
from .vip import get_vip_status


def _cooldown_text(session, is_vip: bool) -> str:
    remaining = image_cooldown_remaining(session, is_vip)
    if remaining <= 0:
        return "🟢 Image Forge Ready"

    mins = remaining // 60
    secs = remaining % 60
    return f"⏳ Cooldown: {mins}m {secs}s"


async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    session = get_session(chat_id)
    vip = await get_vip_status(user.id)

    session["is_vip"] = vip["is_vip"]

    text = (
        "🔥 **MEGAFORGE**\n\n"
        "Forge comic-style art powered by MegaGrok.\n\n"
        "👤 **Your Status**\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if vip['is_vip'] else '🔴 NOT ENABLED'}\n"
        f"{_cooldown_text(session, vip['is_vip'])}\n\n"
        "💡 Wallet linking is handled securely via the VIP bot.\n\n"
        "Choose a forge mode:"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=main_menu(vip["is_vip"])
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    session = get_session(chat_id)
    is_vip = session.get("is_vip", False)

    if query.data == "image_forge":
        await context.bot.send_message(
            chat_id=chat_id,
            text="✏️ Send a prompt for your MegaGrok image."
        )
        session["awaiting_prompt"] = True
        return

    if query.data == "surprise_me":
        if image_cooldown_remaining(session, is_vip) > 0:
            await context.bot.send_message(
                chat_id=chat_id,
                text="⏳ Image Forge is on cooldown. Try again later."
            )
            return

        await context.bot.send_message(
            chat_id=chat_id,
            text="🎨 Forging a surprise MegaGrok image…"
        )

        path = await generate_image(
            prompt="doing something unexpected",
            is_vip=is_vip
        )

        mark_image_used(session)

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=open(path, "rb"),
            caption="🖼 Forge complete.\n\nRun /megaforge again."
        )
        return

    if query.data == "vip_required":
        await context.bot.send_message(
            chat_id=chat_id,
            text="🔒 This forge requires VIP access.\nUse the VIP bot to unlock."
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    session = get_session(chat_id)

    if not session.get("awaiting_prompt"):
        return

    is_vip = session.get("is_vip", False)

    if image_cooldown_remaining(session, is_vip) > 0:
        await update.message.reply_text(
            "⏳ Image Forge is on cooldown. Try again later."
        )
        return

    prompt = update.message.text
    session["awaiting_prompt"] = False

    await update.message.reply_text("🎨 Forging your MegaGrok image…")

    path = await generate_image(prompt, is_vip)
    mark_image_used(session)

    await update.message.reply_photo(
        photo=open(path, "rb"),
        caption="🖼 Forge complete.\n\nRun /megaforge again."
    )

import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image
from bot.utils.vip_manager import load_vip_users
from bot.utils.style import MEGAGROK_STYLE


# ============================
#   /grokposter  (VIP ONLY)
# ============================
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # VIP CHECK
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    if not is_vip:
        return await update.message.reply_text(
            "⚠️ This command is VIP-only.\n"
            "You need to hold MegaGrok tokens or be added manually.\n"
            "🔥 Public free generator is available with /grokfree"
        )

    # USER IDEA
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    # FINAL STYLE PROMPT
    final_prompt = f"""
{MEGAGROK_STYLE}

User idea: {user_idea}
""".strip()

    await update.message.reply_text("🎨 VIP Mode — Generating high-quality MegaGrok poster...")

    try:
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generate_image, final_prompt)

        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        msg = str(e)
        if len(msg) > 900:
            msg = msg[:900] + " ... [truncated]"
        await update.message.reply_text(f"❌ Error: {msg}")


# ============================
#   /grokfree  (OPEN FOR ALL)
# ============================
async def handle_grokfree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = f"""
{MEGAGROK_STYLE}

User idea: {user_idea}
""".strip()

    await update.message.reply_text(
        "🆓 Using FREE fallback generator...\n"
        "🎨 Creating MegaGrok-style artwork..."
    )

    try:
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generate_fallback_image, final_prompt)

        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        msg = str(e)
        if len(msg) > 900:
            msg = msg[:900] + " ... [truncated]"
        await update.message.reply_text(f"❌ Error: {msg}")

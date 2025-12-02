import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image
from bot.utils.vip_manager import load_vip_users
from bot.utils.style import MEGAGROK_STYLE


# -------------------------------------------------
#  MAIN GENERATOR: /grokposter
#  VIP = Stability AI
#  NON-VIP = Free fallback
# -------------------------------------------------
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check VIP list
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    # User input
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    # Inject global style
    final_prompt = f"""
{MEGAGROK_STYLE}

User idea: {user_idea}
""".strip()

    # Feedback to user
    if is_vip:
        await update.message.reply_text("🎨 VIP mode — generating ultra-quality MegaGrok poster...")
    else:
        await update.message.reply_text(
            "🟢 Generating free MegaGrok poster (fallback mode)\n"
            "🔥 Upgrade to VIP for higher quality."
        )

    # Choose generator
    generator = generate_image if is_vip else generate_fallback_image

    try:
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generator, final_prompt)

        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        msg = str(e)
        if len(msg) > 900:
            msg = msg[:900] + " ... [truncated]"
        await update.message.reply_text(f"❌ Error: {msg}")


# -------------------------------------------------
#  FREE TEST COMMAND: /grokfree
#  Always uses fallback generator
# -------------------------------------------------
async def handle_grokfree(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = f"""
{MEGAGROK_STYLE}

User idea: {user_idea}
""".strip()

    await update.message.reply_text("🟢 Free generator activated — generating MegaGrok poster...")

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

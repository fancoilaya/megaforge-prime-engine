import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image

from bot.utils.vip_manager import load_vip_users
from bot.utils.style import VIP_STYLE
from bot.utils.style_free import FREE_STYLE


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

    # User idea text
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    # Select correct style block
    style_block = VIP_STYLE if is_vip else FREE_STYLE

    # CRITICAL FIX: SCENE FIRST, STYLE LAST
    final_prompt = f"""
Scene: {user_idea}

Visual Style Guide:
{style_block}
""".strip()

    # Feedback to user
    if is_vip:
        await update.message.reply_text("🎨 VIP mode — generating ULTRA-quality MegaGrok poster...")
    else:
        await update.message.reply_text(
            "🟢 Free generator activated (community mode)\n"
            "🔥 VIP unlocks MUCH more accurate MegaGrok posters!"
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

    # SCENE FIRST for free generator too
    final_prompt = f"""
Scene: {user_idea}

Visual Style Guide:
{FREE_STYLE}
""".strip()

    await update.message.reply_text("🟢 Free generator test activated — standby...")

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

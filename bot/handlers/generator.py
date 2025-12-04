import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image

from bot.utils.vip_manager import load_vip_users
from bot.utils.style import VIP_STYLE
from bot.utils.style_free import FREE_STYLE


# ================================================================
#  MAIN GENERATOR: /grokposter
#  VIP = Stability AI
#  NON-VIP = Free fallback
# ================================================================
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    # User text
    user_idea = " ".join(context.args) if context.args else "doing something epic"

    # Style block (soft influence only)
    style_block = VIP_STYLE if is_vip else FREE_STYLE

    # =======================================================
    # MAIN FIX: Stability interprets a single strong sentence
    # =======================================================
    final_prompt = (
        f"A retro comic-book illustration of MegaGrok, a muscular green frog "
        f"superhero with glowing orange eyes, {user_idea}. "
        f"Bold line art, dynamic pose, vintage print texture.\n\n"
        f"STYLE NOTES:\n{style_block}"
    )

    # User feedback
    if is_vip:
        await update.message.reply_text("🎨 VIP Mode: Generating Ultra-Quality MegaGrok Poster…")
    else:
        await update.message.reply_text(
            "🟢 Free Mode Active — Community generator\n"
            "🔥 VIP unlocks higher style accuracy."
        )

    # Select engine
    generator = generate_image if is_vip else generate_fallback_image

    # Debug display
    print("\n==============================")
    print("🟦 FINAL PROMPT SENT TO ENGINE")
    print("==============================")
    print(final_prompt)
    print("==============================\n")

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


# ================================================================
#  FREE TEST COMMAND: /grokfree
# ================================================================
async def handle_grokfree(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_idea = " ".join(context.args) if context.args else "doing something heroic"

    final_prompt = (
        f"A retro comic-style drawing of MegaGrok, the heroic frog, {user_idea}. "
        f"Bold ink lines, energetic pose.\n\n"
        f"{FREE_STYLE}"
    )

    await update.message.reply_text("🟢 Free Generator Test — Standby...")

    print("\n==============================")
    print("🟦 FREE MODE PROMPT")
    print("==============================")
    print(final_prompt)
    print("==============================\n")

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

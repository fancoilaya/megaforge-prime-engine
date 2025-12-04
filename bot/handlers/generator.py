import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image

from bot.utils.vip_manager import load_vip_users


# ================================================================
#  MAIN GENERATOR: /grokposter
#  VIP = Stability AI (comic-book style)
#  NON-VIP = Free fallback (Pollinations)
# ================================================================
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    # User-provided idea
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    # ✨ Ultra-clean prompt to avoid overriding user input
    if is_vip:
        final_prompt = (
            "MegaGrok – a muscular green anthropomorphic frog superhero with glowing orange eyes, "
            "heroic proportions, frog hands and frog feet. Retro 1970s comic-book poster style. "
            f"Scene: {user_idea}"
        )
    else:
        final_prompt = (
            f"MegaGrok frog superhero in comic style. Scene: {user_idea}"
        )

    # Telegram user feedback
    if is_vip:
        await update.message.reply_text("🎨 VIP Mode: Generating Ultra-Quality MegaGrok Poster…")
    else:
        await update.message.reply_text(
            "🟢 Free Mode Active — Using community generator\n"
            "🔥 VIP unlocks perfect style accuracy."
        )

    # Pick generator
    generator = generate_image if is_vip else generate_fallback_image

    # Debug print → appears in Render logs
    print("\n==============================")
    print("🟦 FINAL PROMPT SENT")
    print("==============================")
    print(final_prompt)
    print("==============================\n")

    try:
        # Run blocking API call in threadpool
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generator, final_prompt)

        # Send image to Telegram
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

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = (
        f"MegaGrok frog superhero comic style. Scene: {user_idea}"
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

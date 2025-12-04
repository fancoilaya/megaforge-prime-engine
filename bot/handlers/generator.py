import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image
from bot.utils.vip_manager import load_vip_users
from bot.utils.style_free import FREE_STYLE


# ================================================================
#  MAIN GENERATOR: /grokposter
#  VIP = Stability (keep minimal prompt!)
# ================================================================
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    if is_vip:
        # ⭐ VIP MUST stay minimal or Stability ignores user input
        final_prompt = f"MegaGrok frog superhero. Scene: {user_idea}"
    else:
        # ⭐ FREE MODE gets tuned style + user idea
        final_prompt = f"{FREE_STYLE}\nScene: {user_idea}"

    # Notify user
    await update.message.reply_text(
        "🎨 VIP MODE — Testing action…" if is_vip else
        "🟢 Free Mode — Comic Poster Style Active"
    )

    generator = generate_image if is_vip else generate_fallback_image

    # Debug log
    print("\n========== PROMPT SENT ==========")
    print(final_prompt)
    print("=================================\n")

    try:
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generator, final_prompt)

        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


# ================================================================
#  FREE TEST COMMAND /grokfree
# ================================================================
async def handle_grokfree(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = f"{FREE_STYLE}\nScene: {user_idea}"

    await update.message.reply_text("🟢 Free Generator Test — Standby...")

    print("\n========== FREE MODE PROMPT ==========")
    print(final_prompt)
    print("======================================\n")

    try:
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generate_fallback_image, final_prompt)

        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

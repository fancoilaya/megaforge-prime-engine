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
#  NON-VIP = Free fallback (Pollinations)
# ================================================================
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    # User text
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    # Select style
    style_block = VIP_STYLE if is_vip else FREE_STYLE

    # Stability-friendly sandwich format (MANDATORY)
    final_prompt = f"""
MAIN SUBJECT (MANDATORY):
A muscular green anthropomorphic frog superhero named MegaGrok.
MegaGrok MUST always be the main character in the image.
MegaGrok MUST always appear exactly as described:
• Muscular heroic proportions
• Green frog skin with dark blue shading
• Large glowing orange eyes
• Orange/tan chest plates
• Frog mouth, frog hands, frog feet
Never show a human as the main subject.
Never replace MegaGrok.

{style_block}

RENDER THE FOLLOWING SCENE CLEARLY:
{user_idea}
""".strip()

    # Notify user
    if is_vip:
        await update.message.reply_text("🎨 VIP Mode: Generating Ultra-Quality MegaGrok Poster…")
    else:
        await update.message.reply_text(
            "🟢 Free Mode Active — Using community generator\n"
            "🔥 VIP unlocks perfect style accuracy."
        )

    # Pick engine
    generator = generate_image if is_vip else generate_fallback_image

    # Debug print for Render logs
    print("\n==============================")
    print("🟦 FINAL PROMPT USED")
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
#  Always uses fallback engine + free style block
# ================================================================
async def handle_grokfree(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = f"""
MAIN SUBJECT (MANDATORY):
A muscular green anthropomorphic frog superhero named MegaGrok.
MegaGrok MUST appear as the hero and never be replaced.

{FREE_STYLE}

SCENE:
{user_idea}
""".strip()

    await update.message.reply_text("🟢 Free Generator Test — Standby...")

    # Debug logging
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

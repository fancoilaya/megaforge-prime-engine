import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image

from bot.utils.vip_manager import load_vip_users
from bot.utils.style_vip import VIP_STYLE
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

    # Choose style
    style_block = VIP_STYLE if is_vip else FREE_STYLE

    # ---------- MINIMAL, STABILITY-FRIENDLY PROMPT ----------
    final_prompt = (
        "MegaGrok, a muscular green anthropomorphic frog superhero with glowing "
        "orange eyes and orange chest plates. Heroic proportions, frog hands, "
        "frog feet. 1970s retro comic-book poster style with thick black outlines, "
        "bold cel-shading and gritty halftone texture. Fiery orange explosive background.\n\n"
        f"STYLE DETAILS:\n{style_block}\n\n"
        f"SCENE: {user_idea}"
    )
    # ---------------------------------------------------------

    # Notify user
    if is_vip:
        await update.message.reply_text("🎨 VIP Mode: Generating Ultra-Quality MegaGrok Poster…")
    else:
        await update.message.reply_text(
            "🟢 Free Mode Active — Using community generator\n"
            "🔥 VIP unlocks perfect style accuracy."
        )

    # Select engine
    generator = generate_image if is_vip else generate_fallback_image

    # Debug print to Render logs
    print("\n==============================")
    print("🟦 FINAL PROMPT USED (VIP)" if is_vip else "🟦 FINAL PROMPT USED (FREE)")
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

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = (
        "MegaGrok, the muscular green frog superhero. Retro comic-book poster look.\n\n"
        f"STYLE (Free Mode):\n{FREE_STYLE}\n\n"
        f"SCENE: {user_idea}"
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

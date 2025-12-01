import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image
from bot.utils.vip_manager import load_vip_users
from bot.utils.style import MEGAGROK_STYLE


async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # --------------------------
    # VIP CHECK
    # --------------------------
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    # --------------------------
    # STYLE INJECTION
    # --------------------------
    final_prompt = f"""
{MEGAGROK_STYLE}

IMPORTANT: The image must stay in the MEGAGROK universe.
Follow this exact illustrated retro-comic style.
Do NOT render realism or 3D.

USER REQUEST:
{user_idea}
""".strip()

    # Let user know which generator is used
    if is_vip:
        await update.message.reply_text(
            "🟢 **VIP Mode Activated**\n"
            "Generating high-quality MegaGrok poster with Stability AI…"
        )
    else:
        await update.message.reply_text(
            "🟡 **Free Mode Activated**\n"
            "Using FREE generator (Pollinations)\n"
            "Upgrade to VIP for premium Stability-powered posters!"
        )

    # --------------------------
    # SELECT GENERATOR
    # --------------------------
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

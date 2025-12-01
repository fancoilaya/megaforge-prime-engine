# bot/handlers/generator.py

import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.stability_api import generate_image
from bot.utils.vip_manager import load_vip_users
from bot.utils.style import MEGAGROK_STYLE   # <-- NEW


async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # ---------------------------
    # VIP CHECK
    # ---------------------------
    vip_users = load_vip_users()
    if user_id not in vip_users:
        return await update.message.reply_text(
            "⚠️ This command is VIP-only.\n"
            "You need to hold MegaGrok tokens or be added manually.\n"
            "🔥 Public free generator (fallback) is coming soon!"
        )

    # ---------------------------
    # BUILD FINAL PROMPT
    # ---------------------------
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    final_prompt = f"""
{MEGAGROK_STYLE}

User idea: {user_idea}
""".strip()

    # ---------------------------
    # GENERATE IMAGE
    # ---------------------------
    await update.message.reply_text("🎨 Generating MegaGrok Poster... Hold tight!")

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


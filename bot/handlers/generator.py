# bot/handlers/generator.py

import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.stability_api import generate_image
from bot.vip_users import VIP_USERS  # <-- NEW IMPORT


async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # -------------------------
    # 🔐 VIP ACCESS CHECK
    # -------------------------
    if user_id not in VIP_USERS:
        return await update.message.reply_text(
            "⚠️ This command is VIP-only.\n\n"
            "Soon you'll unlock access by linking your wallet 🔗🐸"
        )

    # -------------------------
    # ORIGINAL WORKING CODE
    # -------------------------
    prompt = " ".join(context.args) if context.args else "MegaGrok poster"

    await update.message.reply_text("🎨 Generating Megagrok Poster... Hold tight!")

    try:
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(None, generate_image, prompt)

        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        msg = str(e)
        if len(msg) > 900:
            msg = msg[:900] + " ... [truncated]"

        await update.message.reply_text(f"❌ Error: {msg}")

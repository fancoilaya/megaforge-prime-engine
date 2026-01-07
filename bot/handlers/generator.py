import asyncio
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.services.stability_api import generate_image
from bot.services.fallback_api import generate_fallback_image
from bot.utils.vip_manager import load_vip_users
from bot.utils.style_free import FREE_STYLE

async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    vip_users = load_vip_users()
    is_vip = user_id in vip_users

    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"

    if is_vip:
        final_prompt = f"MegaGrok frog superhero. Scene: {user_idea}"
    else:
        final_prompt = f"{FREE_STYLE}\nScene: {user_idea}"

    await update.message.reply_text(
        "🎨 VIP MODE" if is_vip else "🟢 Free Mode"
    )

    generator = generate_image if is_vip else generate_fallback_image
    loop = asyncio.get_event_loop()
    image_path = await loop.run_in_executor(None, generator, final_prompt)

    with open(image_path, "rb") as img:
        await update.message.reply_photo(photo=img)

async def handle_grokfree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_idea = " ".join(context.args) if context.args else "MegaGrok poster"
    final_prompt = f"{FREE_STYLE}\nScene: {user_idea}"

    loop = asyncio.get_event_loop()
    image_path = await loop.run_in_executor(
        None, generate_fallback_image, final_prompt
    )

    with open(image_path, "rb") as img:
        await update.message.reply_photo(photo=img)

def register(app):
    app.add_handler(CommandHandler("grokposter", handle_grokart))
    app.add_handler(CommandHandler("grokfree", handle_grokfree))

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.stability_api import generate_image

async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args) if context.args else "MegaGrok poster"
    await update.message.reply_text("🎨 Generating MegaGrok poster...")

    try:
        image_path = generate_image(prompt)
        await update.message.reply_photo(photo=open(image_path, "rb"))
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# If you want the command to be /grokposter instead:
# generator_handler = CommandHandler("grokposter", handle_grokart)

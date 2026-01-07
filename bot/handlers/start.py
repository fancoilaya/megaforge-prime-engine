from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 MegaForge Prime Engine Initialized. Use /megaforge to begin."
    )

def register(app):
    app.add_handler(CommandHandler("start", start))

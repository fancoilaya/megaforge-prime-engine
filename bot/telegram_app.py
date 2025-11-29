# bot/telegram_app.py

from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.generator import handle_grokart
from bot.config import TELEGRAM_BOT_TOKEN

def create_application():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # register commands
    app.add_handler(CommandHandler("grokposter", handle_grokart))

    return app

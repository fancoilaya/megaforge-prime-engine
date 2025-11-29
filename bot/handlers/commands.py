from telegram.ext import CommandHandler
from bot.handlers.generator import handle_grokart

def register_commands(app):
    app.add_handler(CommandHandler("grokart", handle_grokart))

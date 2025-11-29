from telegram.ext import CommandHandler
from bot.handlers.generator import handle_grokart




def register_commands(app):commands.py


app.add_handler(CommandHandler("grokart", handle_grokart))

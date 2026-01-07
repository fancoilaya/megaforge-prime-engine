from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters
from .ui import handle_megaforge, handle_callback, handle_text

def register(app):
    app.add_handler(CommandHandler("megaforge", handle_megaforge))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

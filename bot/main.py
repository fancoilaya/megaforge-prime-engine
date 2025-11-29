# bot/main.py

import threading
import logging
import os
import uvicorn

from bot.webserver import app as fastapi_app
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers.generator import handle_grokart

from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(level=logging.INFO)


def start_bot_thread():
    """Runs the Telegram bot in a separate thread."""
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("grokposter", handle_grokart))

    logging.info("Starting Telegram bot polling in thread...")
    app.run_polling()   # <-- NOT awaited, blocks ONLY this thread


def start_web():
    """Starts FastAPI server on main thread."""
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    # Start bot in background thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()

    # Start FastAPI in main thread
    start_web()

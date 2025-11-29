# bot/main.py

import threading
import logging
import os
import uvicorn
import asyncio

from bot.webserver import app as fastapi_app
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers.generator import handle_grokart

from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(level=logging.INFO)


def start_bot_thread():
    """Runs the Telegram bot inside its own event loop in a background thread."""

    # Create event loop for this thread
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("grokposter", handle_grokart))
    app.add_handler(CommandHandler("grokart", handle_grokart))

    logging.info("Starting Telegram bot polling in thread...")

    # Disable signal handlers → REQUIRED to run in threads
    loop.run_until_complete(
        app.run_polling(
            stop_signals=None,           # <-- FIX for your error
            allowed_updates=None,
            drop_pending_updates=True,
        )
    )


def start_web():
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    # Start bot thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()

    # Start FastAPI
    start_web()

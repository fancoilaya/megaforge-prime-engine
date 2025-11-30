# bot/main.py

import threading
import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler
import uvicorn

from bot.webserver import app as fastapi_app
from bot.handlers.generator import handle_grokart
from bot.config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="BOT | %(asctime)s | %(levelname)s | %(message)s"
)


def start_bot_thread():
    """Run Telegram bot in its own thread using its own event loop."""
    logging.info("Starting Telegram bot...")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("grokposter", handle_grokart))

    logging.info("Bot handlers registered. Running polling...")
    app.run_polling()  # BLOCKS only this thread


def start_web():
    """Run FastAPI server on main thread."""
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    # Start bot on background thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()

    # Run FastAPI
    start_web()

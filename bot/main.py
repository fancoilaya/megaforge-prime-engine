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

# Prevent double-start from Uvicorn workers
BOT_STARTED = False


def start_bot():
    global BOT_STARTED
    if BOT_STARTED:
        logging.info("Bot already running, skipping duplicate start.")
        return

    BOT_STARTED = True

    logging.info("Starting Telegram bot polling...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("grokposter", handle_grokart))
    app.run_polling()  # blocking inside this thread only


def start_web():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        workers=1  # << IMPORTANT: ensure single worker
    )


if __name__ == "__main__":
    # Run bot in a background thread
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # Run FastAPI server
    start_web()

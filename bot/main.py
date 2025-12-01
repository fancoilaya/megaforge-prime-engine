import threading
import logging
import os
import asyncio
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
    """Run Telegram bot safely inside its own event loop (Render-safe)."""
    try:
        logging.info("Starting Telegram bot...")

        app = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .build()
        )

        app.add_handler(CommandHandler("grokposter", handle_grokart))

        logging.info("Bot handlers registered. Starting polling loop...")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # SUPER IMPORTANT: disable ALL signal handling
        loop.run_until_complete(app.run_polling(
            allowed_updates=None,
            stop_signals=[]  # ensures no thread crash
        ))

    except Exception as e:
        logging.error(f"BOT THREAD CRASHED: {e}")


def start_web():
    """Run FastAPI/uvicorn in the main thread (Render requirement)."""
    port = int(os.getenv("PORT", 8000))
    logging.info(f"Starting FastAPI server on port {port}")

    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        timeout_keep_alive=30
    )


if __name__ == "__main__":
    # Start Telegram bot in background daemon thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()

    # Start FastAPI in main thread
    start_web()

# bot/main.py
import threading
import logging
import os
import asyncio
import traceback
from telegram.ext import ApplicationBuilder, CommandHandler
import uvicorn

from bot.webserver import app as fastapi_app
from bot.handlers.generator import handle_grokart, handle_grokfree
from bot.handlers.admin import cmd_addvip, cmd_removevip, cmd_viplist
from bot.config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="BOT | %(asctime)s | %(levelname)s | %(message)s"
)


def start_bot_thread():
    """Run Telegram bot safely inside its own event loop (Render-safe)."""
    try:
        logging.info("Starting Telegram bot thread...")

        # build the application
        app = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .build()
        )

        # -----------------------------------------------------
        # COMMAND REGISTRATION (mirror your existing file)
        # -----------------------------------------------------
        app.add_handler(CommandHandler("grokposter", handle_grokart))
        app.add_handler(CommandHandler("grokfree", handle_grokfree))
        app.add_handler(CommandHandler("addvip", cmd_addvip))
        app.add_handler(CommandHandler("removevip", cmd_removevip))
        app.add_handler(CommandHandler("viplist", cmd_viplist))

        logging.info("Bot handlers registered. Preparing event loop for thread...")

        # Create thread-local asyncio loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run polling inside thread and log any exceptions that happen
        try:
            logging.info("Starting polling (thread-local loop).")
            loop.run_until_complete(
                app.run_polling(
                    allowed_updates=None,
                    stop_signals=[]  # prevents thread crashes on Render
                )
            )
            logging.info("Polling finished (clean stop).")
        except Exception as inner_exc:
            logging.error("Exception inside bot polling loop:\n" + "".join(traceback.format_exception(inner_exc)))
        finally:
            # Best-effort shutdown sequence
            try:
                loop.run_until_complete(app.stop())
                loop.run_until_complete(app.shutdown())
            except Exception:
                logging.exception("Error during bot shutdown cleanup.")
            logging.info("Bot thread exiting.")

    except Exception as e:
        logging.error("BOT THREAD CRASHED at startup:\n" + "".join(traceback.format_exception(e)))


def start_web():
    """Run FastAPI/Uvicorn in the main thread (Render requirement)."""
    port = int(os.getenv("PORT", 8000))
    logging.info(f"Starting FastAPI server on port {port}")

    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        timeout_keep_alive=60  # a bit higher keep-alive for long requests
    )


if __name__ == "__main__":
    # Quick preflight checks
    if not TELEGRAM_BOT_TOKEN:
        logging.error("TELEGRAM_BOT_TOKEN is not set. Exiting.")
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN")

    # Start Telegram bot in background daemon thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True, name="telegram-bot-thread")
    bot_thread.start()
    logging.info("Bot thread started (daemon).")

    # Start FastAPI in main thread (blocking)
    start_web()

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
    """Runs Telegram bot safely in its own event loop."""
    try:
        logging.info("Starting Telegram bot thread...")

        app = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .build()
        )

        # -------------------------------------------------
        # REGISTER COMMANDS
        # -------------------------------------------------
        app.add_handler(CommandHandler("grokposter", handle_grokart))
        app.add_handler(CommandHandler("grokfree", handle_grokfree))
        app.add_handler(CommandHandler("addvip", cmd_addvip))
        app.add_handler(CommandHandler("removevip", cmd_removevip))
        app.add_handler(CommandHandler("viplist", cmd_viplist))

        logging.info("Bot handlers registered.")

        # Thread-local event loop (REQUIRED on Render!)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            logging.info("Polling started inside thread.")
            loop.run_until_complete(
                app.run_polling(
                    allowed_updates=None,
                    stop_signals=[]  # prevents Render from killing the thread
                )
            )
        except Exception as exc:
            logging.error("Bot polling crashed:\n" + "".join(traceback.format_exception(exc)))

        finally:
            # Safe shutdown
            try:
                loop.run_until_complete(app.stop())
                loop.run_until_complete(app.shutdown())
            except Exception:
                logging.exception("Error during Telegram bot shutdown cleanup.")

            logging.info("Bot thread exited.")

    except Exception as e:
        logging.error("BOT THREAD FAILED AT STARTUP:\n" + "".join(traceback.format_exception(e)))


def start_web():
    """Runs FastAPI on main thread (Render requires this)."""
    port = int(os.getenv("PORT", 8000))
    logging.info(f"Starting FastAPI server on port {port}")

    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        timeout_keep_alive=90  # Gives model enough time
    )


if __name__ == "__main__":

    if not TELEGRAM_BOT_TOKEN:
        logging.error("Missing TELEGRAM_BOT_TOKEN — exiting.")
        raise SystemExit

    # Start bot thread
    bot_thread = threading.Thread(
        target=start_bot_thread,
        daemon=True,
        name="tg-bot-thread"
    )
    bot_thread.start()
    logging.info("Telegram bot thread started.")

    # Start FastAPI
    start_web()

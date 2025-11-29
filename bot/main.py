import asyncio
import uvicorn
from telegram.ext import ApplicationBuilder

from bot.utils.config import TELEGRAM_BOT_TOKEN, SCHEDULER_ENABLED
from bot.handlers.start import register_start
from bot.handlers.commands import register_commands
from bot.utils.scheduler import init_scheduler
from bot.webserver import app as fastapi_app


async def start_bot():
    print("MegaForge Prime Engine is booting...")

    bot_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    register_start(bot_app)
    register_commands(bot_app)

    if SCHEDULER_ENABLED:
        init_scheduler(bot_app)

    print("MegaForge Prime Engine is online.")

    await bot_app.run_polling()


def start_webserver():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    import threading
    import os

    # Start Telegram bot in background thread
    threading.Thread(target=lambda: asyncio.run(start_bot()), daemon=True).start()

    # Start FastAPI server (mandatory for Render Web Service)
    start_webserver()

# bot/main.py

import asyncio
import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.webserver import app as fastapi_app
from bot.handlers.generator import handle_grokart
from bot.config import TELEGRAM_BOT_TOKEN

import uvicorn

logging.basicConfig(level=logging.INFO)


async def start_bot():
    """Start Telegram bot inside the same event loop."""
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("grokposter", handle_grokart))

    logging.info("Initializing Telegram bot...")
    await app.initialize()
    await app.start()

    logging.info("Starting Telegram updater polling...")
    await app.updater.start_polling()

    logging.info("Bot polling active.")


async def start_web():
    """Run FastAPI with Uvicorn in the shared loop."""
    config = uvicorn.Config(
        fastapi_app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        loop="asyncio",
        lifespan="on"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    bot_task = asyncio.create_task(start_bot())
    web_task = asyncio.create_task(start_web())

    await asyncio.gather(bot_task, web_task)


if __name__ == "__main__":
    asyncio.run(main())

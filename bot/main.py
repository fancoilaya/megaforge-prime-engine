# bot/main.py

import asyncio
import logging
import os

from bot.webserver import app as fastapi_app
import uvicorn

from bot.handlers.generator import handle_grokart
from bot.config import TELEGRAM_BOT_TOKEN

from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(level=logging.INFO)


def build_bot():
    """Create Telegram bot application."""
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("grokposter", handle_grokart))

    return app


async def run_web():
    """Start FastAPI server via uvicorn."""
    port = int(os.getenv("PORT", 8000))

    config = uvicorn.Config(
        fastapi_app,
        host="0.0.0.0",
        port=port,
        loop="asyncio",
        log_level="info",
    )

    server = uvicorn.Server(config)
    await server.serve()


async def run_bot():
    """Start Telegram bot polling."""
    bot_app = build_bot()
    await bot_app.run_polling()  # Correct PTB v20 usage


async def main():
    # Run BOTH services together
    await asyncio.gather(
        run_web(),
        run_bot()
    )


if __name__ == "__main__":
    asyncio.run(main())

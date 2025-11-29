# bot/main.py
import logging
import asyncio

from bot.web import start as start_web
from bot.bot import create_application  # your PTB application factory

logging.basicConfig(level=logging.INFO)

async def start_bot():
    """Start the Telegram bot in the background."""
    app = create_application()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logging.info("Telegram bot started.")

async def main():
    # Start bot task in background
    asyncio.create_task(start_bot())

    # Start the FastAPI web server (blocking)
    start_web()

if __name__ == "__main__":
    asyncio.run(main())

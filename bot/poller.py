# bot/poller.py
import asyncio
import logging
from telegram.ext import Application, CommandHandler
from bot.config import TELEGRAM_TOKEN
from bot.handlers.generator import handle_grokart

logging.basicConfig(level=logging.INFO)

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("grokposter", handle_grokart))

    logging.info("MegaForge Poller: running polling...")
    await app.run_polling(close_loop=False)

def main():
    try:
        loop = asyncio.get_running_loop()
        # Running inside the same event loop → just schedule the coroutine
        loop.create_task(run_bot())
    except RuntimeError:
        # No running loop → start a new one
        asyncio.run(run_bot())

if __name__ == "__main__":
    main()

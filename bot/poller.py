# bot/poller.py

import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers.generator import generator_handler
from bot.utils.config import TELEGRAM_BOT_TOKEN

async def start_polling():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(generator_handler)
    print("MegaForge Poller: running polling...")
    await app.run_polling()

if __name__ == "__main__":
    print("MegaForge Poller: starting (child process)")
    asyncio.run(start_polling())

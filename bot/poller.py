import asyncio
import logging
from bot.config import TELEGRAM_TOKEN
from bot.handlers.generator import generator_handler

from telegram.ext import Application, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_bot():
    logger.info("MegaForge Poller: starting...")

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    # Register handlers
    app.add_handler(CommandHandler("grokposter", generator_handler))

    logger.info("MegaForge Poller: running polling...")

    # This manages its own loop safely when used with asyncio.run()
    await app.run_polling()

def main():
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()

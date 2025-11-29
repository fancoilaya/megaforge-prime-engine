import asyncio
from telegram.ext import ApplicationBuilder

from bot.utils.config import TELEGRAM_BOT_TOKEN, SCHEDULER_ENABLED
from bot.handlers.start import register_start
from bot.handlers.commands import register_commands
from bot.utils.scheduler import init_scheduler


async def main():
    print("MegaForge Prime Engine is booting...")

    # Create the Application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register bot commands & handlers
    register_start(app)
    register_commands(app)

    # Optional scheduler
    if SCHEDULER_ENABLED:
        init_scheduler(app)

    print("MegaForge Prime Engine is online.")
    
    # This starts polling without trying to create or close a new event loop.
    await app.run_polling(close_loop=False)


if __name__ == "__main__":
    # This runs the async main function ONCE, cleanly.
    asyncio.run(main())

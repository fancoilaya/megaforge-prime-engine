import sys
import os

# --- FIX: Ensure project root is in Python path ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
# --------------------------------------------------

from telegram.ext import ApplicationBuilder
from bot.config import TELEGRAM_BOT_TOKEN, SCHEDULER_ENABLED
from bot.handlers.start import register_start
from bot.handlers.commands import register_commands
from bot.utils.scheduler import init_scheduler

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    register_start(app)
    register_commands(app)

    if SCHEDULER_ENABLED:
        init_scheduler(app)

    print("MegaForge Prime Engine is online.")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

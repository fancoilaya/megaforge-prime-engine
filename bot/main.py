from telegram.ext import ApplicationBuilder
from bot.utils.config import TELEGRAM_BOT_TOKEN, SCHEDULER_ENABLED
from bot.handlers.start import register_start
from bot.handlers.commands import register_commands
from bot.utils.scheduler import init_scheduler


def main():
    print("MegaForge Prime Engine is booting...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    register_start(app)
    register_commands(app)

    if SCHEDULER_ENABLED:
        init_scheduler(app)

    print("MegaForge Prime Engine is online.")

    # Sync wrapper. NO event loop issues. Perfect for Render.
    app.run_polling()


if __name__ == "__main__":
    main()

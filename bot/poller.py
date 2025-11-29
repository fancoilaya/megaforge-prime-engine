import logging
from telegram.ext import ApplicationBuilder
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers.generator import generator_handler

logging.basicConfig(level=logging.INFO)


def main():
    print("MegaForge Poller: starting (child process)")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # register handlers
    app.add_handler(generator_handler)

    print("MegaForge Poller: running polling...")
    app.run_polling()  # <-- synchronous, no asyncio, no loop issues


if __name__ == "__main__":
    main()

# bot/main.py

import logging
from telegram.ext import ApplicationBuilder

from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import auto_register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="BOT | %(asctime)s | %(levelname)s | %(message)s"
)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # 🔥 Auto-load ALL handlers
    auto_register_handlers(app)

    logging.info("🚀 Bot starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()

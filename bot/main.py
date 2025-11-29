# bot/main.py

import asyncio
import logging
import os
import uvicorn

from bot.webserver import app as fastapi_app
from bot.telegram_app import create_application

logging.basicConfig(level=logging.INFO)

async def run_web():
    """Start FastAPI using uvicorn inside the same event loop."""
    config = uvicorn.Config(
        fastapi_app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        loop="asyncio",
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

async def run_bot():
    """Start Telegram bot using PTB v20 run_polling()."""
    bot_app = create_application()
    await bot_app.run_polling()

async def main():
    await asyncio.gather(
        run_web(),
        run_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())

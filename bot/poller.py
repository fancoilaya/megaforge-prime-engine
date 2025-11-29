import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers.generator import generator_handler
from bot.config import TELEGRAM_BOT_TOKEN


async def main():
    print("MegaForge Poller: starting (child process)")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(generator_handler)

    print("MegaForge Poller: running polling...")

    # IMPORTANT:
    # PTB manages its own internal event loop – DO NOT wrap it in asyncio.run()
    await app.run_polling(close_loop=False)


if __name__ == "__main__":
    # Run inside existing event loop if any
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        # If no loop exists, create one
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(main())

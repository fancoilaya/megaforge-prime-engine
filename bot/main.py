import asyncio
import uvicorn
from fastapi import FastAPI

from telegram.ext import Application, CommandHandler
from bot.handlers.generator import handle_grokart
from bot.config import TELEGRAM_BOT_TOKEN

app = FastAPI()

@app.get("/")
def root():
    return {"status": "MegaForge Online"}

async def start_bot():
    tg_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("grokart", handle_grokart))

    print("🚀 Starting Telegram polling...")
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()
    return tg_app

async def main():
    bot = await start_bot()

    config = uvicorn.Config(app, host="0.0.0.0", port=10000)
    server = uvicorn.Server(config)

    # run FastAPI & Telegram polling together
    api_task = asyncio.create_task(server.serve())

    await bot.updater.await_stop()  # waits until polling stops
    api_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())

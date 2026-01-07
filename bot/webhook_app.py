# bot/webhook_app.py

import logging
from fastapi import FastAPI, Request, Response

from telegram import Update
from telegram.ext import ApplicationBuilder

from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import auto_register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="BOT | %(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI()
telegram_app = None


@app.on_event("startup")
async def startup():
    global telegram_app

    telegram_app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    auto_register_handlers(telegram_app)
    await telegram_app.initialize()

    logging.info("🚀 Telegram webhook application initialized")


@app.on_event("shutdown")
async def shutdown():
    if telegram_app:
        await telegram_app.shutdown()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return Response(status_code=200)


@app.get("/")
def health():
    return {"service": "MegaForge Webhook Bot", "status": "online"}

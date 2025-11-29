from telegram import Update
from telegram.ext import ContextTypes
from bot.services.megagrok_prompt_builder import build_prompt
from bot.services.stability_api import generate_image
import random


async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
args = context.args


category = args[0] if args else None
flavor = " ".join(args[1:]) if len(args) > 1 else ""


prompt = build_prompt(category, flavor)
await update.message.reply_text(f"⚙️ MegaForge forging: {category or 'random'}...")


image_path = generate_image(prompt)
await update.message.reply_photo(photo=open(image_path, 'rb'))




async def generate_random_art(app, context):
from telegram import Bot
bot = Bot(app.bot.token)


prompt = build_prompt(None, "")
image_path = generate_image(prompt)


await bot.send_photo(chat_id="<YOUR_CHANNEL_ID>", photo=open(image_path, 'rb'))

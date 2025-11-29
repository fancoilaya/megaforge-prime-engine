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

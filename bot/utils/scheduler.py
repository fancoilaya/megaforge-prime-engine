from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.handlers.generator import generate_random_art


scheduler = AsyncIOScheduler()




def init_scheduler(app):
scheduler.add_job(lambda: generate_random_art(app, None), 'cron', hour=9)
scheduler.start()

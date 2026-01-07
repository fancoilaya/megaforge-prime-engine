from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.vip_manager import load_vip_users, add_vip, remove_vip

ADMIN_ID = 7574908943  # <-- YOUR TELEGRAM ID

def is_admin(user_id: int):
    return user_id == ADMIN_ID

async def cmd_addvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    uid = int(context.args[0])
    add_vip(uid)
    await update.message.reply_text(f"✅ Added {uid} as VIP")

async def cmd_removevip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    uid = int(context.args[0])
    remove_vip(uid)
    await update.message.reply_text(f"❌ Removed {uid} from VIP")

async def cmd_viplist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    vip = load_vip_users()
    await update.message.reply_text(str(vip))

def register(app):
    app.add_handler(CommandHandler("addvip", cmd_addvip))
    app.add_handler(CommandHandler("removevip", cmd_removevip))
    app.add_handler(CommandHandler("viplist", cmd_viplist))

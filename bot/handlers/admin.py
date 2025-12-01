from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.vip_manager import load_vip_users, add_vip, remove_vip

# IMPORTANT: your Telegram user ID (the bot owner)
ADMIN_ID = 7574908943  # <-- REPLACE THIS WITH YOUR ID


def is_admin(user_id: int):
    return user_id == ADMIN_ID


async def cmd_addvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ You are not allowed to use this command.")

    if len(context.args) != 1:
        return await update.message.reply_text("Usage: /addvip <telegram_user_id>")

    try:
        uid = int(context.args[0])
    except:
        return await update.message.reply_text("❌ Invalid user ID format.")

    add_vip(uid)
    await update.message.reply_text(f"✅ Added {uid} to VIP list!")


async def cmd_removevip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ You are not allowed to use this command.")

    if len(context.args) != 1:
        return await update.message.reply_text("Usage: /removevip <telegram_user_id>")

    try:
        uid = int(context.args[0])
    except:
        return await update.message.reply_text("❌ Invalid user ID format.")

    remove_vip(uid)
    await update.message.reply_text(f"✅ Removed {uid} from VIP list!")


async def cmd_viplist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ You are not allowed to use this command.")

    vip = load_vip_users()
    if not vip:
        return await update.message.reply_text("VIP list is empty.")

    msg = "✨ **VIP Users:**\n" + "\n".join([f"- `{uid}`" for uid in sorted(vip)])
    await update.message.reply_text(msg, parse_mode="Markdown")

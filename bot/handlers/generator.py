import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.services.stability_api import generate_image


# -------------------------------
#  /grokart command handler
# -------------------------------
async def handle_grokart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # If user wrote: /grokart MegaGroK fighting a bull
        if context.args:
            prompt = " ".join(context.args)
        else:
            await update.message.reply_text(
                "⚡️ *Usage:* `/grokart <your prompt>`\n"
                "Example: `/grokart MegaGrok charging up in neon style`",
                parse_mode="Markdown"
            )
            return

        await update.message.reply_text("🧪 Generating image... Please wait.")

        # Call Stability API
        image_path = generate_image(prompt)

        # Send image back to user
        await update.message.reply_photo(photo=open(image_path, "rb"))

        # Clean up temp file
        try:
            os.remove(image_path)
        except:
            pass

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {type(e).__name__}\n`{str(e)}`",
            parse_mode="Markdown"
        )


# ---------------------------------------------------------
# Exported handler so poller.py can import it cleanly
# ---------------------------------------------------------
generator_handler = CommandHandler("grokart", handle_grokart)

# If you want the command to be /grokposter instead:
# generator_handler = CommandHandler("grokposter", handle_grokart)

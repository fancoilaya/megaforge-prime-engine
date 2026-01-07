# bot/handlers/megaforge_ui.py

import logging
import time
import random
import asyncio
import requests
from enum import Enum, auto
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.services.fallback_api import generate_fallback_image
from bot.services.stability_api import generate_image
from bot.config import VIP_SERVICE_URL
import os

# ------------------------------------------------------------------
# LOGGING (VERY IMPORTANT FOR AUTO-LOADER DEBUGGING)
# ------------------------------------------------------------------

logging.info("📦 Loading megaforge_ui handler module")

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------

VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")

FREE_COOLDOWN = 600   # 10 minutes
VIP_COOLDOWN = 60     # 1 minute

# ------------------------------------------------------------------
# STATE MACHINE
# ------------------------------------------------------------------

class ForgeState(Enum):
    IDLE = auto()
    MAIN_MENU = auto()
    IMAGE_INPUT = auto()
    EXIT = auto()

SESSIONS: Dict[int, Dict[str, Any]] = {}

def get_session(user_id: int) -> Dict[str, Any]:
    if user_id not in SESSIONS:
        SESSIONS[user_id] = {
            "state": ForgeState.IDLE,
            "is_vip": False,
            "last_used": 0,
        }
    return SESSIONS[user_id]

# ------------------------------------------------------------------
# VIP CHECK
# ------------------------------------------------------------------

def check_vip_status(user_id: int) -> bool:
    if not VIP_SERVICE_API_KEY:
        return False

    try:
        r = requests.get(
            f"{VIP_SERVICE_URL}/vip/status",
            params={"telegram_id": user_id},
            headers={"Authorization": f"Bearer {VIP_SERVICE_API_KEY}"},
            timeout=5,
        )
        return bool(r.json().get("is_vip", False))
    except Exception:
        return False

# ------------------------------------------------------------------
# COOLDOWN
# ------------------------------------------------------------------

def cooldown_remaining(session: Dict[str, Any]) -> int:
    now = int(time.time())
    cooldown = VIP_COOLDOWN if session["is_vip"] else FREE_COOLDOWN
    return max(0, cooldown - (now - session["last_used"]))

# ------------------------------------------------------------------
# UI
# ------------------------------------------------------------------

def main_menu(is_vip: bool):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Image Forge", callback_data="mf_image")],
        [InlineKeyboardButton("🎲 Chaos Forge", callback_data="mf_chaos")],
        [InlineKeyboardButton(
            "✨ VIP Forge" if is_vip else "✨ VIP Forge 🔒",
            callback_data="mf_vip"
        )],
        [InlineKeyboardButton("❌ Exit", callback_data="mf_exit")],
    ])

# ------------------------------------------------------------------
# ENTRY POINT (/megaforge)
# ------------------------------------------------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    session["is_vip"] = check_vip_status(user_id)
    session["state"] = ForgeState.MAIN_MENU

    await update.message.reply_text(
        f"🔥 **MEGAFORGE ONLINE**\n\n"
        f"Status: {'✨ VIP' if session['is_vip'] else '🟢 Free'}\n\n"
        f"Choose a forge mode:",
        reply_markup=main_menu(session["is_vip"]),
        parse_mode="Markdown"
    )

# ------------------------------------------------------------------
# CALLBACK HANDLER
# ------------------------------------------------------------------

async def handle_megaforge_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = get_session(user_id)

    if query.data == "mf_exit":
        session["state"] = ForgeState.EXIT
        await query.edit_message_text("🧱 MegaForge closed.")
        return

    if query.data == "mf_image":
        session["state"] = ForgeState.IMAGE_INPUT
        await query.edit_message_text(
            "🎨 **IMAGE FORGE**\n\n"
            "Describe what MegaGrok is doing.\n"
            "Comic style is always applied.",
            parse_mode="Markdown"
        )
        return

    if query.data == "mf_chaos":
        await run_generation(query, session, random_chaos_prompt())
        return

    if query.data == "mf_vip":
        if not session["is_vip"]:
            await query.edit_message_text(
                "🔒 **VIP FORGE LOCKED**\n\n"
                "Hold the MegaGrok token to unlock.\n"
                "Wallet linking happens privately.",
                parse_mode="Markdown"
            )
            return

        await query.edit_message_text(
            "✨ **VIP FORGE**\n\n"
            "Advanced generation enabled.",
            reply_markup=main_menu(True),
            parse_mode="Markdown"
        )
        return

# ------------------------------------------------------------------
# TEXT INPUT HANDLER
# ------------------------------------------------------------------

async def handle_megaforge_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if session["state"] != ForgeState.IMAGE_INPUT:
        return

    prompt = update.message.text.strip()
    await run_generation(update, session, prompt)

# ------------------------------------------------------------------
# GENERATION CORE
# ------------------------------------------------------------------

async def run_generation(source, session: Dict[str, Any], prompt: str):
    remaining = cooldown_remaining(session)
    if remaining > 0:
        msg = f"⏳ Cooldown active: {remaining}s remaining"
        if hasattr(source, "edit_message_text"):
            await source.edit_message_text(msg)
        else:
            await source.message.reply_text(msg)
        return

    generator = generate_image if session["is_vip"] else generate_fallback_image
    final_prompt = f"MegaGrok comic book style. {prompt}"

    if hasattr(source, "edit_message_text"):
        await source.edit_message_text("🧨 Forging...")
    else:
        await source.message.reply_text("🧨 Forging...")

    loop = asyncio.get_event_loop()
    image_path = await loop.run_in_executor(None, generator, final_prompt)

    session["last_used"] = int(time.time())
    session["state"] = ForgeState.MAIN_MENU

    with open(image_path, "rb") as img:
        await source.message.reply_photo(
            photo=img,
            reply_markup=main_menu(session["is_vip"])
        )

# ------------------------------------------------------------------
# CHAOS PROMPTS
# ------------------------------------------------------------------

def random_chaos_prompt() -> str:
    chaos = [
        "cosmic courtroom collapse",
        "neon arena showdown",
        "psychedelic meme explosion",
        "apex grok ascension",
    ]
    return f"MegaGrok in a {random.choice(chaos)}"

# ------------------------------------------------------------------
# HANDLER REGISTRATION (CRITICAL)
# ------------------------------------------------------------------

from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

def register(app):
    app.add_handler(CommandHandler("megaforge", handle_megaforge))
    app.add_handler(CallbackQueryHandler(handle_megaforge_callback))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_megaforge_text)
    )

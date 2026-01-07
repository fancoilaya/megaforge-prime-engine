# bot/handlers/megaforge_ui.py

import logging
import time
import random
import asyncio
import requests
import os
from enum import Enum, auto
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.services.fallback_api import generate_fallback_image
from bot.services.stability_api import generate_image
from bot.config import VIP_SERVICE_URL

# ------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------

logging.info("📦 Loading megaforge_ui (persistent session model)")

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------

VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")

FREE_COOLDOWN = 600     # 10 minutes
VIP_COOLDOWN = 60       # 1 minute

SESSION_VERSION = 1
SESSION_TTL = 1800      # 30 minutes

# ------------------------------------------------------------------
# STATE MACHINE
# ------------------------------------------------------------------

class ForgeState(Enum):
    IDLE = auto()
    MAIN_MENU = auto()
    IMAGE_INPUT = auto()
    EXIT = auto()

# ------------------------------------------------------------------
# SESSION STORAGE (IN-MEMORY, REDIS-READY)
# ------------------------------------------------------------------

SESSIONS: Dict[int, Dict[str, Any]] = {}

def new_session(user_id: int) -> Dict[str, Any]:
    return {
        "version": SESSION_VERSION,
        "owner_id": user_id,

        "state": ForgeState.MAIN_MENU,
        "active_mode": None,

        "is_vip": False,
        "engine": "free",

        "last_prompt": None,
        "last_used": int(time.time()),

        "cooldowns": {
            "image": 0,
            "meme": 0,
            "sticker": 0,
        },

        "ui": {
            "last_message_type": "text",
        },
    }

def get_session(user_id: int) -> Dict[str, Any]:
    now = int(time.time())
    session = SESSIONS.get(user_id)

    if not session:
        session = new_session(user_id)
        SESSIONS[user_id] = session
        return session

    if session.get("owner_id") != user_id:
        session = new_session(user_id)
        SESSIONS[user_id] = session
        return session

    if session.get("version") != SESSION_VERSION:
        session = new_session(user_id)
        SESSIONS[user_id] = session
        return session

    if now - session.get("last_used", 0) > SESSION_TTL:
        session = new_session(user_id)
        SESSIONS[user_id] = session
        return session

    return session

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
# COOLDOWNS
# ------------------------------------------------------------------

def image_cooldown_remaining(session: Dict[str, Any]) -> int:
    now = int(time.time())
    cooldown = VIP_COOLDOWN if session["is_vip"] else FREE_COOLDOWN
    return max(0, cooldown - (now - session["cooldowns"]["image"]))

# ------------------------------------------------------------------
# UI COMPONENTS
# ------------------------------------------------------------------

def main_menu(is_vip: bool):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Image Forge", callback_data="mf_image")],
        [InlineKeyboardButton("😈 Meme Forge 🔒", callback_data="mf_meme")],
        [InlineKeyboardButton("🧩 Sticker Forge 🔒", callback_data="mf_sticker")],
        [InlineKeyboardButton("🎛 Presets 🔒", callback_data="mf_presets")],
        [InlineKeyboardButton("❌ Exit", callback_data="mf_exit")],
    ])

def vip_locked_message():
    return (
        "🔒 **VIP FORGE LOCKED**\n\n"
        "This forge requires VIP access.\n\n"
        "VIP unlocks:\n"
        "• High-quality image rendering\n"
        "• Faster cooldowns\n"
        "• Meme & Sticker Forge\n"
        "• Presets & future tools\n\n"
        "[ 🔗 Link Wallet to Enable VIP ]"
    )

async def safe_reply(source, text, **kwargs):
    try:
        if hasattr(source, "edit_message_text"):
            await source.edit_message_text(text, **kwargs)
        else:
            await source.message.reply_text(text, **kwargs)
    except Exception:
        await source.message.reply_text(text, **kwargs)

# ------------------------------------------------------------------
# /megaforge ENTRY POINT
# ------------------------------------------------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)
    session["last_used"] = int(time.time())

    session["is_vip"] = check_vip_status(user_id)
    session["engine"] = "vip" if session["is_vip"] else "free"
    session["state"] = ForgeState.MAIN_MENU

    status_block = (
        "━━━━━━━━━━━━━━━━━━\n"
        "👤 **Your Status**\n\n"
        f"VIP ACCESS: {'🟢 ENABLED' if session['is_vip'] else '🔴 NOT ENABLED'}\n"
        f"Image Forge: {'✨ High Quality' if session['is_vip'] else '🟢 Standard Quality'}\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    await update.message.reply_text(
        "🔥 **MEGAFORGE**\n\n"
        "The MegaForge is a creative engine powered by MegaGrok.\n"
        "Here you forge comic-style art, memes, stickers, and viral content —\n"
        "all centered around the Grok universe.\n\n"
        f"{status_block}\n\n"
        "Choose a forge mode:",
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
    session["last_used"] = int(time.time())

    if query.data == "mf_exit":
        session["state"] = ForgeState.EXIT
        await safe_reply(query, "🧱 MegaForge closed.")
        return

    if query.data == "mf_image":
        session["state"] = ForgeState.IMAGE_INPUT
        await safe_reply(
            query,
            "🖼 **IMAGE FORGE**\n\n"
            "Describe what MegaGrok is doing.\n"
            "Comic book style is always applied.",
            parse_mode="Markdown"
        )
        return

    if query.data in ("mf_meme", "mf_sticker", "mf_presets"):
        if not session["is_vip"]:
            await safe_reply(query, vip_locked_message(), parse_mode="Markdown")
            return

        await safe_reply(query, "✨ VIP forge coming online soon.")
        return

# ------------------------------------------------------------------
# TEXT INPUT HANDLER
# ------------------------------------------------------------------

async def handle_megaforge_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)
    session["last_used"] = int(time.time())

    if session["state"] != ForgeState.IMAGE_INPUT:
        return

    prompt = update.message.text.strip()
    await run_image_generation(update, session, prompt)

# ------------------------------------------------------------------
# IMAGE GENERATION
# ------------------------------------------------------------------

async def run_image_generation(source, session: Dict[str, Any], prompt: str):
    remaining = image_cooldown_remaining(session)
    if remaining > 0:
        await safe_reply(source, f"⏳ Cooldown active: {remaining}s remaining")
        return

    await safe_reply(source, "🧨 Forging image...")

    generator = generate_image if session["is_vip"] else generate_fallback_image
    final_prompt = f"MegaGrok comic book style. {prompt}"

    loop = asyncio.get_event_loop()
    image_path = await loop.run_in_executor(None, generator, final_prompt)

    session["cooldowns"]["image"] = int(time.time())
    session["state"] = ForgeState.MAIN_MENU

    with open(image_path, "rb") as img:
        await source.message.reply_photo(
            photo=img,
            reply_markup=main_menu(session["is_vip"])
        )

# ------------------------------------------------------------------
# HANDLER REGISTRATION
# ------------------------------------------------------------------

def register(app):
    app.add_handler(CommandHandler("megaforge", handle_megaforge))
    app.add_handler(CallbackQueryHandler(handle_megaforge_callback))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_megaforge_text)
    )

# MegaForge UI State Machine
# --------------------------
# Public creative UI + private VIP actions
# Free users -> Pollinations
# VIP users  -> Stability.ai
#
# Requires:
# - VIP service running
# - Pollinations generator
# - Stability generator
#
# This file is intentionally explicit and readable.
import logging
logging.info("📦 Loading megaforge_ui handler module")
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
from bot.config import VIP_SERVICE_URL, VIP_SERVICE_API_KEY

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------

FREE_COOLDOWN = 600      # 10 minutes
VIP_COOLDOWN = 60        # 1 minute (adjust later)

# ------------------------------------------------------------------
# STATE ENUM
# ------------------------------------------------------------------

class ForgeState(Enum):
    IDLE = auto()
    MAIN_MENU = auto()
    IMAGE_INPUT = auto()
    CHAOS_CONFIRM = auto()
    MEME_MENU = auto()
    STICKER_MENU = auto()
    INSPIRE_MENU = auto()
    VIP_MENU = auto()
    EXIT = auto()

# ------------------------------------------------------------------
# SESSION STORE (IN-MEMORY)
# ------------------------------------------------------------------

SESSIONS: Dict[int, Dict[str, Any]] = {}

def get_session(user_id: int) -> Dict[str, Any]:
    if user_id not in SESSIONS:
        SESSIONS[user_id] = {
            "state": ForgeState.IDLE,
            "is_vip": False,
            "last_used": 0,
            "payload": {},
        }
    return SESSIONS[user_id]

# ------------------------------------------------------------------
# VIP CHECK
# ------------------------------------------------------------------

def check_vip_status(user_id: int) -> bool:
    try:
        res = requests.get(
            f"{VIP_SERVICE_URL}/vip/status",
            params={"telegram_id": user_id},
            headers={"Authorization": f"Bearer {VIP_SERVICE_API_KEY}"},
            timeout=5,
        )
        data = res.json()
        return bool(data.get("is_vip", False))
    except Exception:
        return False

# ------------------------------------------------------------------
# COOLDOWN
# ------------------------------------------------------------------

def cooldown_remaining(session: Dict[str, Any]) -> int:
    now = int(time.time())
    cooldown = VIP_COOLDOWN if session["is_vip"] else FREE_COOLDOWN
    remaining = cooldown - (now - session["last_used"])
    return max(0, remaining)

# ------------------------------------------------------------------
# UI HELPERS
# ------------------------------------------------------------------

def main_menu_keyboard(is_vip: bool):
    buttons = [
        [InlineKeyboardButton("🖼 Image Forge", callback_data="forge_image")],
        [InlineKeyboardButton("🎲 Chaos Forge", callback_data="forge_chaos")],
        [InlineKeyboardButton("😂 Meme Forge", callback_data="forge_meme")],
        [InlineKeyboardButton("🧩 Sticker Forge", callback_data="forge_sticker")],
        [
            InlineKeyboardButton(
                "✨ VIP Forge" if is_vip else "✨ VIP Forge 🔒",
                callback_data="forge_vip"
            )
        ],
        [InlineKeyboardButton("🔑 VIP Status", callback_data="vip_status")],
        [InlineKeyboardButton("❌ Exit", callback_data="forge_exit")],
    ]
    return InlineKeyboardMarkup(buttons)

# ------------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------------

async def handle_megaforge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = get_session(user.id)

    # Check VIP ONCE per session start
    session["is_vip"] = check_vip_status(user.id)
    session["state"] = ForgeState.MAIN_MENU

    text = (
        "🔥 **MEGAFORGE ONLINE**\n\n"
        "Create. Experiment. Share.\n\n"
        f"Status: {'✨ VIP' if session['is_vip'] else '🟢 Free'}"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu_keyboard(session["is_vip"]),
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

    data = query.data

    # ---------------- EXIT ----------------
    if data == "forge_exit":
        session["state"] = ForgeState.EXIT
        await query.edit_message_text("🧱 MegaForge closed.")
        return

    # ---------------- IMAGE FORGE ----------------
    if data == "forge_image":
        session["state"] = ForgeState.IMAGE_INPUT
        await query.edit_message_text(
            "🎨 **IMAGE FORGE**\n\n"
            "Describe what MegaGrok is doing.\n"
            "Comic style is locked — everything else is free.",
            parse_mode="Markdown"
        )
        return

    # ---------------- CHAOS ----------------
    if data == "forge_chaos":
        session["state"] = ForgeState.CHAOS_CONFIRM
        await query.edit_message_text(
            "🎲 **CHAOS FORGE**\n\n"
            "You are about to generate something unpredictable.\n"
            "MegaGrok will appear. Everything else is chaos.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Forge Chaos", callback_data="chaos_go")],
                [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data == "chaos_go":
        await run_generation(query, session, random_chaos_prompt())
        return

    # ---------------- MEME ----------------
    if data == "forge_meme":
        session["state"] = ForgeState.MEME_MENU
        await query.edit_message_text(
            "😂 **MEME FORGE**\n\nChoose a meme type:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🖼 Image + Text", callback_data="meme_image")],
                [InlineKeyboardButton("🎭 Reaction Meme", callback_data="meme_reaction")],
                [InlineKeyboardButton("🎲 Random Meme", callback_data="meme_random")],
                [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data.startswith("meme_"):
        prompt = f"MegaGrok comic meme, {data.replace('meme_', '')}"
        await run_generation(query, session, prompt)
        return

    # ---------------- STICKER ----------------
    if data == "forge_sticker":
        session["state"] = ForgeState.STICKER_MENU
        await query.edit_message_text(
            "🧩 **STICKER FORGE**\n\nChoose sticker style:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("😈 Expression", callback_data="sticker_expression")],
                [InlineKeyboardButton("😂 Reaction", callback_data="sticker_reaction")],
                [InlineKeyboardButton("🔥 Action", callback_data="sticker_action")],
                [InlineKeyboardButton("🎲 Random", callback_data="sticker_random")],
                [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data.startswith("sticker_"):
        prompt = f"MegaGrok comic sticker, {data.replace('sticker_', '')}"
        await run_generation(query, session, prompt)
        return

    # ---------------- VIP STATUS ----------------
    if data == "vip_status":
        if query.message.chat.type != "private":
            await query.edit_message_text(
                "🔒 VIP actions are handled in private.\n"
                "I’ve sent you a DM for security."
            )
            await context.bot.send_message(
                chat_id=user_id,
                text="✨ **MegaGrok VIP**\n\n"
                     f"Status: {'✨ VIP' if session['is_vip'] else '❌ Not VIP'}\n\n"
                     "Wallet linking is optional and private.\n"
                     "Use this chat to manage VIP.",
                parse_mode="Markdown"
            )
            return

        session["state"] = ForgeState.VIP_MENU
        await query.edit_message_text(
            f"✨ **MEGAGROK VIP**\n\n"
            f"Status: {'✨ VIP' if session['is_vip'] else '❌ Not VIP'}\n\n"
            "• Faster cooldowns\n"
            "• Stability.ai generations\n"
            "• Canon tools (soon)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Link Wallet", callback_data="vip_link")],
                [InlineKeyboardButton("🔍 Refresh Status", callback_data="vip_refresh")],
                [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data == "vip_refresh":
        session["is_vip"] = check_vip_status(user_id)
        await handle_megaforge(update, context)
        return

    # ---------------- BACK ----------------
    if data == "back_main":
        session["state"] = ForgeState.MAIN_MENU
        await query.edit_message_text(
            "🔥 **MEGAFORGE**",
            reply_markup=main_menu_keyboard(session["is_vip"]),
            parse_mode="Markdown"
        )
        return

# ------------------------------------------------------------------
# MESSAGE HANDLER (TEXT INPUT)
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
        await source.edit_message_text(
            f"⏳ Forge cooldown: {remaining}s remaining"
        )
        return

    await source.edit_message_text("🧨 Forging...")

    generator = generate_image if session["is_vip"] else generate_fallback_image
    final_prompt = f"MegaGrok comic book style. {prompt}"

    loop = asyncio.get_event_loop()
    image_path = await loop.run_in_executor(None, generator, final_prompt)

    session["last_used"] = int(time.time())
    session["state"] = ForgeState.MAIN_MENU

    with open(image_path, "rb") as img:
        await source.message.reply_photo(
            photo=img,
            reply_markup=main_menu_keyboard(session["is_vip"])
        )

# ------------------------------------------------------------------
# CHAOS PROMPTS
# ------------------------------------------------------------------

def random_chaos_prompt() -> str:
    chaos = [
        "cosmic horror courtroom",
        "medieval dragon battle",
        "psychedelic meme explosion",
        "fallen angel judge",
        "arena announcer losing sanity",
    ]
    return f"MegaGrok in a {random.choice(chaos)}"

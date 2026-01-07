import time
from enum import Enum, auto
from typing import Dict, Any

SESSION_VERSION = 1
SESSION_TTL = 1800  # 30 minutes

class ForgeState(Enum):
    IDLE = auto()
    MAIN_MENU = auto()
    IMAGE_INPUT = auto()
    EXIT = auto()

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

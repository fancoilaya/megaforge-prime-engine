import os
import requests
import logging
from typing import Dict, Any

from bot.config import VIP_SERVICE_URL

VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")

def fetch_vip_status(telegram_id: int) -> Dict[str, Any]:
    """
    Fetch full VIP status from vip.megagrok.dev
    Returns a dict usable directly by UI & generators.
    """

    # Safe default (never crash MegaForge)
    default = {
        "is_vip": False,
        "wallet": None,
        "sol_balance": 0.0,
        "token_balance": 0.0,
        "token_mint": None,
    }

    if not VIP_SERVICE_API_KEY:
        logging.warning("VIP_SERVICE_API_KEY missing")
        return default

    try:
        r = requests.get(
            f"{VIP_SERVICE_URL}/vip/status",
            params={"telegram_id": telegram_id},
            headers={"Authorization": f"Bearer {VIP_SERVICE_API_KEY}"},
            timeout=5,
        )

        if r.status_code != 200:
            logging.warning(f"VIP service returned {r.status_code}")
            return default

        data = r.json()

        return {
            "is_vip": bool(data.get("is_vip", False)),
            "wallet": data.get("wallet"),
            "sol_balance": float(data.get("sol_balance", 0)),
            "token_balance": float(data.get("token_balance", 0)),
            "token_mint": data.get("token_mint"),
        }

    except Exception as e:
        logging.exception("VIP service error")
        return default

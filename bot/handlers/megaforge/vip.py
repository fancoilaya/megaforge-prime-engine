import os
import requests
from bot.config import VIP_SERVICE_URL

VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")

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

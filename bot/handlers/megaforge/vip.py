import os
import requests

VIP_SERVICE_URL = os.getenv("VIP_SERVICE_URL")
VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {VIP_SERVICE_API_KEY}",
    "Content-Type": "application/json",
}


def get_vip_status(telegram_id: int) -> dict:
    """
    Return VIP status for a Telegram user.
    MegaForge only cares about is_vip.
    """
    if not VIP_SERVICE_URL or not VIP_SERVICE_API_KEY:
        return {"is_vip": False}

    try:
        r = requests.get(
            f"{VIP_SERVICE_URL}/vip/status",
            params={"telegram_id": telegram_id},
            headers=HEADERS,
            timeout=5,
        )

        if r.status_code != 200:
            return {"is_vip": False}

        return {"is_vip": bool(r.json().get("is_vip", False))}

    except Exception:
        return {"is_vip": False}

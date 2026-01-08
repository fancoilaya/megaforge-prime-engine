import os
import requests

VIP_SERVICE_URL = os.getenv("VIP_SERVICE_URL")
VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")


def get_vip_status(telegram_id: int) -> dict:
    """
    Fetch VIP status from the VIP service.
    Always returns a safe dict.
    """
    if not VIP_SERVICE_URL or not VIP_SERVICE_API_KEY:
        return {
            "is_vip": False,
            "source": "missing_config",
        }

    try:
        resp = requests.get(
            f"{VIP_SERVICE_URL}/status/{telegram_id}",
            headers={
                "X-API-Key": VIP_SERVICE_API_KEY,
            },
            timeout=5,
        )

        if resp.status_code != 200:
            return {
                "is_vip": False,
                "source": "vip_service_error",
            }

        data = resp.json()

        return {
            "is_vip": bool(data.get("is_vip", False)),
            "source": "vip_service",
        }

    except Exception:
        return {
            "is_vip": False,
            "source": "vip_service_exception",
        }

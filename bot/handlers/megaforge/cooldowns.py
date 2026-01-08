import time

# seconds
FREE_COOLDOWN = 60 * 60        # 1 hour
VIP_COOLDOWN = 20 * 60         # 20 minutes


def image_cooldown_remaining(session: dict) -> int:
    """
    Returns remaining cooldown in seconds.
    0 means ready.
    """

    last_used = session.get("cooldowns", {}).get("image", 0)
    now = int(time.time())

    vip_info = session.get("vip", {})
    is_vip = vip_info.get("is_vip", False)

    cooldown = VIP_COOLDOWN if is_vip else FREE_COOLDOWN
    remaining = cooldown - (now - last_used)

    return max(0, remaining)

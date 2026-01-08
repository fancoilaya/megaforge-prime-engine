import time

# cooldowns in seconds
FREE_COOLDOWN = 60 * 60        # 1 hour
VIP_COOLDOWN = 20 * 60         # 20 minutes


def image_cooldown_remaining(session: dict, is_vip: bool) -> int:
    """
    Returns remaining cooldown in seconds.
    0 means ready.
    """
    last_used = session.get("last_image_time")

    if not last_used:
        return 0

    cooldown = VIP_COOLDOWN if is_vip else FREE_COOLDOWN
    elapsed = int(time.time() - last_used)

    remaining = cooldown - elapsed
    return max(0, remaining)


def mark_image_used(session: dict):
    """
    Mark the current time as last image usage.
    """
    session["last_image_time"] = int(time.time())

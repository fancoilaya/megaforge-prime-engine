import time

# Cooldown durations (seconds)
FREE_COOLDOWN = 60 * 60      # 1 hour
VIP_COOLDOWN = 20 * 60       # 20 minutes

# In-memory cooldown store
_last_image_time: dict[int, int] = {}


def image_cooldown_remaining(user_id: int, is_vip: bool) -> int | None:
    """
    Returns remaining cooldown in seconds, or None if no cooldown.
    """
    cooldown = VIP_COOLDOWN if is_vip else FREE_COOLDOWN

    last_used = _last_image_time.get(user_id)
    if last_used is None:
        return None

    elapsed = int(time.time()) - last_used
    remaining = cooldown - elapsed

    return remaining if remaining > 0 else None


def mark_image_used(user_id: int):
    """
    Marks image usage timestamp for cooldown tracking.
    """
    _last_image_time[user_id] = int(time.time())

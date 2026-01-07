import time

FREE_COOLDOWN = 600
VIP_COOLDOWN = 60

def image_cooldown_remaining(session: dict) -> int:
    now = int(time.time())
    cooldown = VIP_COOLDOWN if session["is_vip"] else FREE_COOLDOWN
    return max(0, cooldown - (now - session["cooldowns"]["image"]))

# bot/config.py

import os

# --------------------------------------------------
# EXISTING CONFIG (UNCHANGED)
# --------------------------------------------------

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "false").lower() == "true"

# --------------------------------------------------
# VIP SERVICE CONFIG (NEW – REQUIRED FOR MEGAFORGE)
# --------------------------------------------------

VIP_SERVICE_URL = os.getenv(
    "VIP_SERVICE_URL",
    "https://vip.megagrok.dev"
)

VIP_SERVICE_API_KEY = os.getenv("VIP_SERVICE_API_KEY")

# --------------------------------------------------
# SAFETY CHECKS
# --------------------------------------------------

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

# VIP is required for MegaForge
if not VIP_SERVICE_API_KEY:
    raise RuntimeError("Missing VIP_SERVICE_API_KEY")

# Stability is optional (Free users still work)
if not STABILITY_API_KEY:
    print("⚠️ WARNING: STABILITY_API_KEY not set — VIP image generation disabled.")

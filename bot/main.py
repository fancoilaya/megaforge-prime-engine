# bot/main.py
from fastapi import FastAPI
from bot.webserver import app  # << correct import

# No telegram bot here
# No asyncio
# No polling
# This file is ONLY the FastAPI server entry point

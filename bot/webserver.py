# bot/web.py
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "online", "message": "MegaForge Telegram Bot API"}

def start():
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

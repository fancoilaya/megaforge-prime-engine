# bot/main.py
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "MegaForge Prime Engine is online"}

if __name__ == "__main__":
    uvicorn.run("bot.main:app", host="0.0.0.0", port=10000)

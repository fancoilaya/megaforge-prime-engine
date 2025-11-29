import subprocess
from fastapi import FastAPI
from bot.server import app  # FIXED: correct import


def start_poller():
    print("Starting poller subprocess...")
    subprocess.Popen(
        ["python", "-m", "bot.poller"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


# Start poller when FastAPI boots
@app.on_event("startup")
def startup_event():
    print("MegaForge Prime Engine is booting...")
    start_poller()
    print("MegaForge Prime Engine is online.")


# This allows: python -m bot.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

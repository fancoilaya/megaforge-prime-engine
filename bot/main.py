import subprocess
import uvicorn
from bot.web import app  # Your FastAPI app


def start_poller():
    """
    Launch the Telegram bot poller as a separate OS process.
    This prevents event-loop conflicts with Uvicorn.
    """
    print("Starting MegaForge Poller (subprocess)...")
    subprocess.Popen(
        ["python", "-m", "bot.poller"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


if __name__ == "__main__":
    # Start the Telegram poller in the background
    start_poller()

    print("MegaForge Prime Engine (webserver) is online.")

    # Launch FastAPI via Uvicorn (Render will bind to PORT)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=10000,   # Render exposes this automatically
        log_level="info"
    )

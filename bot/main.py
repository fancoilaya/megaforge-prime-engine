# bot/main.py
import os
import subprocess
from bot.webserver import app as fastapi_app
import uvicorn

def start_poller_process():
    # Launch the poller as a separate python process (module)
    # Use -u to make stdout/stderr unbuffered so logs appear in Render immediately
    cmd = [os.sys.executable, "-u", "-m", "bot.poller"]
    print("Starting poller subprocess:", cmd)
    # note: do NOT wait(); keep it running. We don't need to capture output here.
    return subprocess.Popen(cmd)

def main():
    # Start poller child process
    proc = start_poller_process()

    # Start fastapi in this (main) process so Render detects port
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

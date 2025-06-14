# Auto install dependencies before bot starts
import os
import subprocess
import sys

def install_requirements():
    flag_file = ".requirements_installed"
    if not os.path.exists(flag_file):
        print("[INFO] Installing dependencies from requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"])
            open(flag_file, "w").close()
            print("[INFO] Requirements installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install requirements: {e}")
            sys.exit(1)
    else:
        print("[INFO] Requirements already installed.")

install_requirements()

# --------- Your original async bot starts here ---------

import asyncio
from shared_client import start_client
import importlib

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass

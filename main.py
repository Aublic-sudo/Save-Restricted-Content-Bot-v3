# main.py

# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client, app
import importlib
import os
import sys

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
    print("✅ Bot is alive. Listening for commands...")

    # This keeps Pyrogram running and handles updates
    await app.start()
    await asyncio.get_event_loop().create_future()  # Keeps it alive

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("🚀 Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass

import asyncio

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from nc_py_api import NextcloudApp
from nc_py_api.ex_app import AppAPIAuthMiddleware, run_app, set_handlers

from utils.db import get_db_connection, create_tables, is_file_processed
from forms import SETTINGS_FORM
from utils.nc import get_nextcloud_app, get_setings
from utils.queue import queue_file, is_file_queued


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.ensure_future(watch_files())
    set_handlers(app, enabled_handler)
    yield

db = get_db_connection()
create_tables(db)

APP = FastAPI(lifespan=lifespan)
APP.add_middleware(AppAPIAuthMiddleware)

IMG_EXTENSIONS = ["png", "jpg", "jpeg"]


async def watch_files():
    nc = get_nextcloud_app()

    minutes = float(get_setings(nc, 'scan_interval', 1))
    while True:
        enabled = get_setings(nc, 'enabled', False)

        if enabled:
            print(f"[WATCHER] Scanning for new files every {minutes} minutes...", flush=True)
            minutes = float(get_setings(nc, 'scan_interval', 1))
            scan_path = get_setings(nc, 'scan_path', '/')

            for f in nc.files.listdir(scan_path, depth=-1):
                if not Path(f.user_path).suffix.lower()[1:] in IMG_EXTENSIONS:
                    print(f"[WATCHER] Skipping non-image file: {f.user_path}", flush=True)
                    continue

                if is_file_queued(f.user_path) or is_file_processed(db, f.user_path):
                    print(f"[WATCHER] Skipping: {is_file_queued(f.user_path)}, {is_file_processed(db, f.user_path)}", flush=True)
                    continue

                queue_file(f.user_path)

        await asyncio.sleep(minutes * 60)  # Convert minutes to seconds


def enabled_handler(enabled: bool, nc: NextcloudApp) -> str:
    try:
        if enabled:
            nc.ui.settings.register_form(SETTINGS_FORM)
            print("App enabled, saving timestamp to file and registering settings form.")
        else:
            nc.ui.settings.unregister_form('settings_example')
    except Exception as e:
        print(f"Error in enabled_handler: {e}")
        return str(e)
    return ""


if __name__ == "__main__":
    run_app(
        "main:APP",
        log_level="trace",
    )

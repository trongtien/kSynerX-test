from pathlib import Path

import uvicorn
from core.config import cdms_setting

ROOT_DIR = Path(__file__).resolve().parent


def start():
    uvicorn.run(
        "app.app:cdms_app_main",
        host=cdms_setting.SERVICE_HOST,
        port=cdms_setting.SERVICE_PORT,
        reload=True,
        app_dir=str(ROOT_DIR),
        reload_dirs=[str(ROOT_DIR)],
    )


if __name__ == "__main__":
    start()

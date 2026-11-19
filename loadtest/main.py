import os
import sys
from pathlib import Path

import uvicorn
from core.config import cdms_setting

ROOT_DIR = Path(__file__).resolve().parent
CDMS_DIR = ROOT_DIR.parent / "cdms"
sys.path.insert(0, str(CDMS_DIR))


def start() -> None:
    uvicorn.run(
        "server_test:app",
        host=cdms_setting.SERVICE_TEST_HOST,
        port=int(cdms_setting.SERVICE_TEST_PORT),
        app_dir=str(ROOT_DIR),
    )


if __name__ == "__main__":
    start()

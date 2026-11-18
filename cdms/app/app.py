from contextlib import asynccontextmanager

from app.api.health_check import root_router
from core.config import cdms_setting
from core.database import DatabaseProvider
from fastapi import FastAPI


@asynccontextmanager
async def lifespan_database(app: FastAPI):
    DatabaseProvider.check_database_connection()
    yield
    DatabaseProvider.shutdown_database()


cdms_app_main = FastAPI(
    title=cdms_setting.SERVICE_NAME,
    version=cdms_setting.SERVICE_VERSION,
    lifespan=lifespan_database,
)

cdms_app_main.include_router(router=root_router)

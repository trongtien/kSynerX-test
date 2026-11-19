from contextlib import asynccontextmanager

from app.api.health_check import root_router
from app.api.product_import_excel import product_import_excel_router
from app.api.product_web_hook import product_web_hook_router
from app.services.product_pull_service import ProductPullService
from core.config import cdms_setting
from core.database import DatabaseProvider, SessionLocal
from core.load_test_http import LoadTestHttp
from core.scheduler import ProductPullScheduler
from fastapi import FastAPI


@asynccontextmanager
async def lifespan_database(app: FastAPI):  # pyright: ignore[reportUnusedParameter]
    DatabaseProvider.check_database_connection()

    load_test_client = LoadTestHttp()
    scheduler = ProductPullScheduler(
        pull_service=ProductPullService(
            session_factory=SessionLocal,
            load_test_client=load_test_client,
            page_size=cdms_setting.PULL_PRODUCT_PAGE_SIZE,
            max_page=cdms_setting.PULL_PRODUCT_MAX_PAGE,
        ),
        interval_seconds=cdms_setting.PULL_PRODUCT_INTERVAL_SECONDS,
    )
    scheduler.start()

    yield

    await scheduler.stop()
    load_test_client.close()
    DatabaseProvider.shutdown_database()


cdms_app_main = FastAPI(
    title=cdms_setting.SERVICE_NAME,
    version=cdms_setting.SERVICE_VERSION,
    lifespan=lifespan_database,
)

cdms_app_main.include_router(router=root_router)
cdms_app_main.include_router(router=product_web_hook_router)
cdms_app_main.include_router(router=product_import_excel_router)

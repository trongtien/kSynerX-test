from core.config import cdms_setting
from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "project": cdms_setting.SERVICE_NAME,
        "version": cdms_setting.SERVICE_VERSION,
    }

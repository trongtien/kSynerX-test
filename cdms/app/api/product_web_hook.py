from app.enums.source_type_enum import SourceTypeEnum
from app.requests.webhook_product_request import WebHookProductRequest
from app.services.product_hash_service import ProductHashService
from app.services.product_process_service import ProductProcessService
from core.database import DatabaseSession
from core.logger import logger
from fastapi import APIRouter, HTTPException

product_web_hook_router = APIRouter(prefix="/webhook", tags=["Product"])


@product_web_hook_router.post(
    "/products", summary="Receive Real-time Product Changes via Webhook"
)
def webhook_receive_product(
    body: WebHookProductRequest,
    connection: DatabaseSession,
):
    try:
        products = body.mapper_product_builder(update_at=None)

        process_service = ProductProcessService(
            connection=connection, product_hash_service=ProductHashService()
        )
        result_service = process_service.execute(
            products=products,
            source_type=SourceTypeEnum.WEBHOOK,
        )

        return result_service
    except OSError as e:
        logger.error(f"Shutting down database \n --> {e}")
        connection.rollback()
        msg = f"{e}"
        raise HTTPException(
            status_code=500, detail=f"Failed to process webhook data: \n {msg}"
        )

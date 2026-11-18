from app.requests.webhook_product_request import WebHookProductRequest
from app.services.product_process_service import ProductProcessService
from core.database import DatabaseSession
from core.logger import logger
from fastapi import APIRouter, HTTPException

product_web_hook_router = APIRouter(prefix="/webhook", tags=["Product"])


@product_web_hook_router.post(
    "/products", summary="Receive Real-time Product Changes via Webhook"
)
def webhook_receive_product(
    body: list[WebHookProductRequest],
    connection: DatabaseSession,
):
    try:
        items_dict = [item.model_dump() for item in body]

        logger.info("Body request")
        logger.info(f"--> {items_dict}")

        process_service = ProductProcessService(connection=connection)
        result_service = process_service.execute(items_dict)

        return result_service
    except OSError as e:
        logger.error(f"Shutting down database \n --> {e}")
        connection.rollback()
        msg = f"{e}"
        raise HTTPException(
            status_code=500, detail=f"Failed to process webhook data: \n {msg}"
        )

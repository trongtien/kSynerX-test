from app.requests.webhook_product_request import WebHookProductRequest
from core.database import DatabaseSession
from fastapi import APIRouter, HTTPException

product_web_hook_router = APIRouter(prefix="/webhook", tags=["Product webhook"])


@product_web_hook_router.post(
    "/products", summary="Receive Real-time Product Changes via Webhook"
)
def webhook_receive_product(
    body: list[WebHookProductRequest],
    connection: DatabaseSession,
):
    try:
        items_dict = [item.model_dump() for item in body]

        return {}
    except Exception as e:
        connection.rollback()
        msg = f"{e}"
        raise HTTPException(
            status_code=500, detail=f"Failed to process webhook data: \n {msg}"
        )

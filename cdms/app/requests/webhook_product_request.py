from datetime import UTC, datetime

from app.requests.product_request import ProductRequest
from app.utils.product_builder_factory import ProductBuilder
from pydantic import BaseModel, Field


class WebHookProductRequest(BaseModel):
    products: list[ProductRequest] = Field(min_length=1, max_length=5000)

    def mapper_product_builder(
        self, update_at: datetime | None
    ) -> list[ProductBuilder]:
        now_at = update_at or datetime.now(UTC)
        return [item.mapper_product_builder(now_at) for item in self.products]

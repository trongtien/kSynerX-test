from datetime import datetime

from app.requests.category_request import CategoryRequest
from app.utils.product_builder_factory import ProductBuilder
from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=100)
    product_name: str = Field(alias="productName", min_length=1, max_length=255)
    product_id: int | None = Field(default=None, alias="productId")
    partner_sku: str | None = Field(default=None, alias="partnerSKU", max_length=100)
    asset_type: str | None = Field(default=None, alias="assetType", max_length=30)
    color: str | None = Field(default=None, max_length=100)
    size: str | None = Field(default=None, max_length=100)
    description: str | None = None
    is_active: bool = Field(default=True, alias="isActive")
    has_serial: bool = Field(default=False, alias="hasSerial")
    has_expiration: bool = Field(default=False, alias="hasExpiration")
    units: list[str] = Field(default_factory=list)
    categories: list[CategoryRequest] = Field(default_factory=list)

    def mapper_product_builder(self, source_updated_at: datetime) -> ProductBuilder:
        return ProductBuilder(
            sku=self.sku,
            product_name=self.product_name,
            source_updated_at=source_updated_at,
            product_id=self.product_id,
            partner_sku=self.partner_sku,
            asset_type=self.asset_type,
            color=self.color,
            size=self.size,
            description=self.description,
            is_active=self.is_active,
            has_serial=self.has_serial,
            has_expiration=self.has_expiration,
            units=tuple(self.units),
            categories=tuple(c.mapper_category_item() for c in self.categories),
        )

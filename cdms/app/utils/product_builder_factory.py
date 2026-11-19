from dataclasses import dataclass
from datetime import datetime

from app.utils.format_str import FormatString


@dataclass(frozen=True, slots=True)
class CategoryItem(FormatString):
    category_code: str
    category_name: str | None = None

    def __init__(self):
        code = self.tranform_text(self.category_code)
        if code is None:
            raise ValueError("categoryCode must not be empty")

        name = self.tranform_text(self.category_name)

        object.__setattr__(self, "category_code", code)
        object.__setattr__(self, "category_name", name)


class ProductBuilder(FormatString):
    sku: str
    product_name: str
    source_updated_at: datetime
    product_id: int | None = None
    partner_sku: str | None = None
    asset_type: str | None = None
    color: str | None = None
    size: str | None = None
    description: str | None = None
    is_active: bool = True
    has_serial: bool = False
    has_expiration: bool = False
    units: tuple[str, ...] = ()
    categories: tuple[CategoryItem, ...] = ()

    def __init__(self):
        sku = self.tranform_text(self.sku)
        if sku is None:
            raise ValueError("Sku must not be empty")

        product_name = self.tranform_text(self.product_name)
        if product_name is None:
            raise ValueError("Product name must not be empty")

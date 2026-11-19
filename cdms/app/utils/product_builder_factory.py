from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.utils.format_str import FormatString


@dataclass(frozen=True, slots=True)
class CategoryItem(FormatString):
    category_code: str
    category_name: str | None = None

    def __post_init__(self) -> None:
        code = self.tranform_text(self.category_code)
        if code is None:
            raise ValueError("categoryCode must not be empty")

        name = self.tranform_text(self.category_name)

        object.__setattr__(self, "category_code", code)
        object.__setattr__(self, "category_name", name)


@dataclass(frozen=True, slots=True)
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

    def __post_init__(self) -> None:
        sku = self.tranform_text(self.sku)
        if sku is None:
            raise ValueError("Sku must not be empty")

        product_name = self.tranform_text(self.product_name)
        if product_name is None:
            raise ValueError("Product name must not be empty")

        if self.source_updated_at.tzinfo is None:
            raise ValueError("Source updated at must be timezone-aware")

        units = self._tranform_format_unit(self.units)
        categories = self._tranform_format_category(self.categories)

        object.__setattr__(self, "sku", sku)
        object.__setattr__(self, "product_name", product_name)
        object.__setattr__(self, "units", units)
        object.__setattr__(self, "categories", categories)

    @staticmethod
    def comapare_old(
        old_change: dict[str, Any], next_change: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        changes = {}

        for field, new_value in next_change.items():
            old_value = old_change.get(field)

            if old_value == new_value:
                continue

            changes[field] = {
                "old": old_value,
                "new": new_value,
            }

        return changes

    def snap_dumps(self) -> dict[str, Any]:
        return {
            "sku": self.sku,
            "partner_sku": self.partner_sku,
            "product_name": self.product_name,
            "asset_type": self.asset_type,
            "color": self.color,
            "size": self.size,
            "description": self.description,
            "is_active": self.is_active,
            "has_serial": self.has_serial,
            "has_expiration": self.has_expiration,
            "units": list(self.units),
            "categories": [
                {"categoryCode": c.category_code, "categoryName": c.category_name}
                for c in self.categories
            ],
        }

    def _tranform_format_unit(self, value: tuple[str, ...]) -> tuple[str, ...]:
        cleaned_units: set[str] = set()
        for unit in value:
            cleaned_unit = self.tranform_text(unit)
            if cleaned_unit:
                cleaned_units.add(cleaned_unit)

        return tuple(sorted(cleaned_units))

    def _tranform_format_category(
        self, value: tuple[CategoryItem, ...]
    ) -> tuple[CategoryItem, ...]:
        unique_categories: dict[str, CategoryItem] = {}

        for category in value:
            unique_categories[category.category_code] = category

        categories = sorted(
            unique_categories.values(),
            key=lambda category: category.category_code,
        )

        return tuple(categories)

from app.utils.product_builder_factory import CategoryItemBuilder
from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    category_code: str = Field(alias="categoryCode", min_length=1, max_length=100)
    category_name: str | None = Field(
        default=None, alias="categoryName", max_length=255
    )

    def mapper_category_item(self) -> CategoryItemBuilder:
        return CategoryItemBuilder(
            category_name=self.category_name, category_code=self.category_code
        )

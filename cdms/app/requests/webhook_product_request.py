from pydantic import BaseModel, Field


class WebHookProductRequest(BaseModel):
    sku: str
    name: str
    price: float = Field(ge=0, description="Price product >= 0")

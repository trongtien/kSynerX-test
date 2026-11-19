from pydantic import BaseModel


class WebHookProductRequest(BaseModel):
    sku: str
    name: str

import os
from typing import Annotated, Any

from core.path_request import FAKE_PRODUCT_VIETFULL
from fastapi import FastAPI, Query
from product import ProductFaker

app = FastAPI(title="Service Load test")


faker = ProductFaker(seed=42)
for _ in range(int(os.getenv("INITIAL_PRODUCTS", "250"))):
    faker.new_product()


@app.get(FAKE_PRODUCT_VIETFULL)
def list_products(
    page_index: Annotated[int, Query(alias="PageIndex", ge=0)] = 0,
    page_size: Annotated[int, Query(alias="PageSize", ge=1, le=1000)] = 10,
) -> list[dict[str, Any]]:
    products = sorted(faker.products.values(), key=lambda p: p["productId"])
    start = page_index * page_size
    return products[start : start + page_size]

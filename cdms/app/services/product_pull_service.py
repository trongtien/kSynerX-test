from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any

from app.enums.source_type_enum import SourceTypeEnum
from app.requests.product_request import ProductRequest
from app.services.product_hash_service import ProductHashService
from app.services.product_process_service import ProductProcessService
from app.utils.product_builder_factory import ProductBuilder
from core.load_test_http import LoadTestHttp
from core.logger import logger
from sqlalchemy.orm import Session


@dataclass()
class PullParams:
    pages: int = 0
    received: int = 0
    invalid: int = 0
    duplicated: int = 0
    saved: int = 0


class ProductPullService:
    def __init__(
        self,
        session_factory: Callable[[], Session],
        load_test_client: LoadTestHttp,
        page_size: int,
        max_page: int,
    ):
        self.session_factory = session_factory
        self.load_test_client = load_test_client
        self.page_size = page_size
        self.max_page = max_page

    def run_pull_product(self) -> PullParams:
        """
        -> Pull every page from the source first
        -> Format data (same rules as ExcelFileService):
            -> validate, trim value, remove row missing sku / product_name
            -> upper sku
            -> remove row duplicate sku (keep last)
        -> Push everything into ProductProcessService in one call
        """
        polled_at = datetime.now(UTC)
        summary = PullParams()

        items = self._fetch_all_items(summary)
        products = self._to_products(items, polled_at, summary)
        products = self._remove_duplicate_sku(products, summary)

        if not products:
            logger.warning("Polling finished with no valid product to save")
            return summary

        with self.session_factory() as session:
            ProductProcessService(
                connection=session, product_hash_service=ProductHashService()
            ).execute(
                products=products,
                source_type=SourceTypeEnum.POLLING,
                dict_check_skus=[p.sku for p in products],
            )

        summary.saved = len(products)
        return summary

    def _fetch_all_items(self, summary: PullParams) -> list[dict[str, Any]]:
        all_items: list[dict[str, Any]] = []

        for page_index in range(self.max_page):
            items = self.load_test_client.exec(page_index, self.page_size) or []
            all_items.extend(items)

            summary.pages += 1
            summary.received += len(items)

            is_skip_next = len(items) < self.page_size
            if is_skip_next:
                break
        else:
            logger.warning(f"Pull product stopped at the page limit ({self.max_page})")

        return all_items

    def _to_products(
        self,
        items: list[dict[str, Any]],
        polled_at: datetime,
        summary: PullParams,
    ) -> list[ProductBuilder]:
        products: list[ProductBuilder] = []
        for position, item in enumerate(items):
            try:
                request = ProductRequest.model_validate(item)
                product = request.mapper_product_builder(polled_at)
                products.append(replace(product, sku=product.sku.upper()))
            except ValueError as e:
                summary.invalid += 1
                logger.warning(f"Skip invalid product (item {position}): {e}")
        return products

    def _remove_duplicate_sku(
        self, products: list[ProductBuilder], summary: PullParams
    ) -> list[ProductBuilder]:
        unique: dict[str, ProductBuilder] = {}
        for product in products:
            if unique.pop(product.sku, None) is not None:
                summary.duplicated += 1
            unique[product.sku] = product
        return list(unique.values())

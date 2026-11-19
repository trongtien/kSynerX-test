import hashlib
from datetime import UTC, datetime
from decimal import Decimal

from app.enums.change_type_enum import ChangeTypeEnum
from app.models.product_audit_log_model import ProductAuditLogModel
from app.models.product_model import ProductModel
from core.logger import logger
from sqlalchemy import insert, update
from sqlalchemy.orm import Session


class ProductProcessService:
    def __init__(self, connection: Session) -> None:
        self.connection = connection

    def execute(
        self,
        products: list[dict],
        dict_check_skus: list[str] | None = None,
    ) -> None:
        if dict_check_skus is None:
            sku_for_products = [item["sku"] for item in products]
            dict_check_skus = list(set(sku_for_products))

        dict_sku_product = self._get_dict_product_with_sku(dict_check_skus)
        now = datetime.now(UTC)
        raw_insert: list[dict] = []
        raw_udpate: list[dict] = []
        audit_rows: list[dict] = []

        skip_count: int = 0

        for item in products:
            sku: str = item["sku"]
            name: str = item["name"]
            price = Decimal(str(item["price"]))

            new_hash = self._hashing_check(sku=sku, name=name, price=price)
            logger.info(f"Product hashing check {new_hash}")
            product = dict_sku_product.get(sku)

            logger.info(f"Product check exist {products is None}")

            if product is None:
                raw_insert.append(
                    {
                        "sku": sku,
                        "name": name,
                        "price": price,
                        "checksum_hash": new_hash,
                    }
                )

                audit_rows.append(
                    {
                        "sku": sku,
                        "change_type": ChangeTypeEnum.CREATED.value,
                        "details": {"name": name, "price": f"{price:.2f}"},
                        "created_at": now,
                    }
                )

            elif product.checksum_hash != new_hash:
                raw_udpate.append(
                    {
                        "sku": sku,
                        "name": name,
                        "price": price,
                        "checksum_hash": new_hash,
                        "updated_at": now,
                    }
                )

                audit_raw_detail: dict[str, dict[str, str]] = {}
                if product.name != name:
                    audit_raw_detail["name"] = {"old": product.name, "new": name}
                if Decimal(product.price) != price:
                    audit_raw_detail["price"] = {
                        "old": f"{product.price:.2f}",
                        "new": f"{price:.2f}",
                    }

                audit_rows.append(
                    {
                        "sku": sku,
                        "change_type": ChangeTypeEnum.CREATED.value,
                        "details": audit_raw_detail,
                        "created_at": now,
                    }
                )
            else:
                skip_count += 1

        if raw_insert:
            self.connection.execute(insert(ProductModel), raw_insert)
        if raw_udpate:
            self.connection.execute(update(ProductModel), raw_udpate)
        if audit_rows:
            self.connection.execute(insert(ProductAuditLogModel), audit_rows)

        self.connection.commit()

    def _get_dict_product_with_sku(self, skus: list[str]) -> dict[str, ProductModel]:
        existing: dict[str, ProductModel] = {
            product.sku: product
            for product in self.connection.query(ProductModel).filter(
                ProductModel.sku.in_(skus)
            )
        }

        return existing

    def _hashing_check(self, sku: str, name: str, price: Decimal) -> str:
        raw_data_string = f"{sku}|{name}|{price:.2f}"
        return hashlib.sha256(raw_data_string.encode("utf-8")).hexdigest()

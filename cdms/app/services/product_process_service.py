import hashlib
from decimal import Decimal

from app.enums.change_type_enum import ChangeTypeEnum
from app.models.product_audit_log_model import ProductAuditLogModel
from app.models.product_model import ProductModel
from core.logger import logger
from sqlalchemy.orm import Session


class ProductProcessService:
    def __init__(self, connection: Session) -> None:
        self.connection = connection
        self.created_count = 0
        self.updated_count = 0
        self.skip_count = 0

    def execute(self, products: list[dict]) -> None:
        dict_sku_product = self._get_dict_product_with_sku(products)

        for item in products:
            sku: str = item["sku"]
            name: str = item["name"]
            price = Decimal(str(item["price"]))

            new_hash = self._hashing_check(sku=sku, name=name, price=price)
            logger.info(f"Product hashing check {new_hash}")
            product = dict_sku_product.get(sku)

            logger.info(f"Product check exist {products is None}")

            if product is None:
                dict_sku_product[sku] = self._create_product(
                    new_hash=new_hash, sku=sku, name=name, price=price
                )
            elif product.checksum_hash != new_hash:
                self._update_product(
                    product=product, new_hash=new_hash, name=name, price=price
                )
            else:
                self.skip_count += 1

        self.connection.commit()

    def _get_dict_product_with_sku(
        self, products: list[dict]
    ) -> dict[str, ProductModel]:
        skus = {item["sku"] for item in products}
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

    def _create_product(
        self, new_hash: str, sku: str, name: str, price: Decimal
    ) -> ProductModel:
        logger.info("Run create product")
        product = ProductModel(
            sku=sku,
            name=name,
            price=price,
            checksum_hash=new_hash,
        )
        product.changes.append(
            ProductAuditLogModel(
                change_type=ChangeTypeEnum.CREATED.value,
                details={"name": name, "price": f"{price:.2f}"},
            )
        )
        self.connection.add(product)
        self.created_count += 1
        return product

    def _update_product(
        self, product: ProductModel, new_hash: str, name: str, price: Decimal
    ):
        details: dict[str, dict[str, str]] = {}

        if product.name != name:
            details["name"] = {"old": product.name, "new": name}
        if Decimal(product.price) != price:
            details["price"] = {"old": f"{product.price:.2f}", "new": f"{price:.2f}"}

        product.name = name
        product.price = price
        product.checksum_hash = new_hash
        product.changes.append(
            ProductAuditLogModel(
                change_type=ChangeTypeEnum.UPDATED.value, details=details
            )
        )
        self.updated_count += 1

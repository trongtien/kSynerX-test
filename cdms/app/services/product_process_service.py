from typing import Any

from app.enums.change_type_enum import ChangeTypeEnum
from app.enums.source_type_enum import SourceTypeEnum
from app.models import IngestionLogModel, ProductAuditLogModel
from app.models.product_model import ProductModel
from app.services.excel_file_service import ProductBuilder
from app.services.product_hash_service import ProductHashService
from sqlalchemy import insert, update
from sqlalchemy.orm import Session


class ProductProcessService:
    def __init__(self, connection: Session, product_hash_service: ProductHashService):
        self.connection = connection
        self.product_hash_service = product_hash_service

    def execute(
        self,
        products: list[ProductBuilder],
        source_type: SourceTypeEnum,
        dict_check_skus: list[str] | None = None,
    ) -> None:
        total_records = len(products)

        if dict_check_skus is None:
            sku_for_products = [item.sku for item in products]
            dict_check_skus = list(set(sku_for_products))

        ingestion_log = IngestionLogModel(
            source_type=source_type,
            status="RUNING",
            total_records=total_records,
        )

        self.connection.add(ingestion_log)
        self.connection.flush()

        dict_sku_product = self._get_dict_product_with_sku(dict_check_skus)

        raw_insert: list[dict[str, Any]] = []
        raw_udpate: list[dict[str, Any]] = []

        raw_product_audit: list[dict] = []

        for item in products:
            product = dict_sku_product.get(item.sku)
            new_hash = self.product_hash_service.hash_dict(item.snap_dumps())
            product_audit = ProductAuditLogModel(
                sku=item.sku,
                source_type=source_type,
                ingestion_id=ingestion_log.id,
                event_key=source_type,
                checksum_hash=new_hash,
                source_updated_at=item.source_updated_at,
            )
            if product is None:
                raw_insert.append(
                    self._to_raw_model_product(item, new_hash, source_type)
                )

                product_audit.change_type = ChangeTypeEnum.CREATED
                product_audit.details = item.snap_dumps()
                raw_product_audit.append(product_audit.model_dums())
            elif (
                product.checksum_hash != new_hash
                and item.source_updated_at > product.source_updated_at
            ):
                raw_udpate.append(
                    self._to_raw_model_product(item, new_hash, source_type)
                )

                product_audit.change_type = ChangeTypeEnum.UPDATED
                product_audit.details = item.comapare_old(product.snap_dumps())
                raw_product_audit.append(product_audit.model_dums())
            else:
                continue

        total_created = len(raw_insert)
        total_update = len(raw_udpate)
        total_raw_product_audit = len(raw_product_audit)
        total_skip = total_records - total_created - total_update

        ingestion_log.created_count = total_created
        ingestion_log.updated_count = total_update
        ingestion_log.skipped_count = total_skip
        ingestion_log.status = "SUCCESS"

        if total_created:
            self.connection.execute(insert(ProductModel), raw_insert)
        if total_update:
            self.connection.execute(update(ProductModel), raw_udpate)
        if total_raw_product_audit > 0:
            self.connection.execute(insert(ProductAuditLogModel), raw_product_audit)

        self.connection.commit()

    def _get_dict_product_with_sku(self, skus: list[str]) -> dict[str, ProductModel]:
        existing: dict[str, ProductModel] = {
            product.sku: product
            for product in self.connection.query(ProductModel).filter(
                ProductModel.sku.in_(skus)
            )
        }

        return existing

    def _to_raw_model_product(
        self, b: ProductBuilder, checksum_hash: str, source_type: SourceTypeEnum
    ) -> dict[str, Any]:
        return {
            "sku": b.sku,
            "product_id": b.product_id,
            "partner_sku": b.partner_sku,
            "product_name": b.product_name,
            "asset_type": b.asset_type,
            "color": b.color,
            "size": b.size,
            "description": b.description,
            "is_active": b.is_active,
            "has_serial": b.has_serial,
            "has_expiration": b.has_expiration,
            "units": list(b.units),
            "categories": [
                {"categoryCode": c.category_code, "categoryName": c.category_name}
                for c in b.categories
            ],
            "checksum_hash": checksum_hash,
            "source_updated_at": b.source_updated_at,
            "last_source": source_type,
        }

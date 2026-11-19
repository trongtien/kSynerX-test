from datetime import datetime
from typing import Any

from app.enums.change_type_enum import ChangeTypeEnum
from app.enums.source_type_enum import SourceTypeEnum
from app.models.ingestion_log_model import IngestionLogModel
from app.models.product_model import ProductModel
from app.models.sql_alschemy_type import pg_enum
from core.database import BaseSchema
from sqlalchemy import CHAR, BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProductAuditLogModel(BaseSchema):
    __tablename__ = "product_audit_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sku: Mapped[str] = mapped_column(
        String(100), ForeignKey("products.sku", ondelete="RESTRICT")
    )
    change_type: Mapped[ChangeTypeEnum] = mapped_column(
        pg_enum(ChangeTypeEnum, "audit_log_change_type_enum")
    )
    source_type: Mapped[SourceTypeEnum] = mapped_column(
        pg_enum(SourceTypeEnum, "audit_log_source_type_enum")
    )
    ingestion_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("ingestion_logs.id")
    )
    event_key: Mapped[str | None] = mapped_column(String(255))
    checksum_hash: Mapped[str] = mapped_column(CHAR(64))
    details: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    source_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    product: Mapped[ProductModel] = relationship(back_populates="audit_logs")
    ingestion: Mapped[IngestionLogModel | None] = relationship(
        back_populates="audit_logs"
    )

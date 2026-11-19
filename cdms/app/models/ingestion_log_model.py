from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from app.enums.source_type_enum import SourceTypeEnum
from app.models.sql_alschemy_type import pg_enum
from core.database import BaseSchema
from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.product_audit_log_model import ProductAuditLogModel


class IngestionLogModel(BaseSchema):
    __tablename__ = "ingestion_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    source_type: Mapped[SourceTypeEnum] = mapped_column(
        pg_enum(SourceTypeEnum, "source_type_enum")
    )
    status: Mapped[str] = mapped_column(String(30))
    total_records: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    updated_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    skipped_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    audit_logs: Mapped[list[ProductAuditLogModel]] = relationship(
        back_populates="ingestion"
    )

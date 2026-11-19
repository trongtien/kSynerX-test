from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from app.enums.source_type_enum import SourceTypeEnum
from app.models.sql_alschemy_type import pg_enum
from core.database import BaseSchema
from sqlalchemy import (
    CHAR,
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    false,
    func,
    text,
    true,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.product_audit_log_model import ProductAuditLogModel


class ProductModel(BaseSchema):
    __tablename__ = "products"

    sku: Mapped[str] = mapped_column(String(100), primary_key=True)
    product_id: Mapped[int | None] = mapped_column(Integer)
    partner_sku: Mapped[str | None] = mapped_column(String(100))
    product_name: Mapped[str] = mapped_column(String(255))
    asset_type: Mapped[str | None] = mapped_column(String(30))
    color: Mapped[str | None] = mapped_column(String(100))
    size: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    has_serial: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false()
    )
    has_expiration: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false()
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )

    units: Mapped[list[str]] = mapped_column(
        JSONB, default=list, server_default=text("'[]'::jsonb")
    )
    categories: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, default=list, server_default=text("'[]'::jsonb")
    )

    checksum_hash: Mapped[str] = mapped_column(CHAR(64))
    source_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_source: Mapped[SourceTypeEnum] = mapped_column(
        pg_enum(SourceTypeEnum, "product_last_source_enum")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    audit_logs: Mapped[list[ProductAuditLogModel]] = relationship(
        back_populates="product", passive_deletes="all"
    )

    def snap_dumps(self) -> dict[str, Any]:
        return {
            "sku": self.sku,
            "product_id": self.product_id,
            "partner_sku": self.partner_sku,
            "product_name": self.product_name,
            "asset_type": self.asset_type,
            "color": self.color,
            "size": self.size,
            "description": self.description,
            "is_active": self.is_active,
            "has_serial": self.has_serial,
            "has_expiration": self.has_expiration,
            "units": list(self.units or []),
            "categories": list(self.categories or []),
        }

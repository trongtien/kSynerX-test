from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from core.database import BaseSchema
from sqlalchemy import Boolean, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.product_audit_log_model import ProductAuditLogModel


class ProductModel(BaseSchema):
    __tablename__ = "products"
    sku: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    parner_sku: Mapped[str | None] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    checksum_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    changes: Mapped[list[ProductAuditLogModel]] = relationship(
        "ProductAuditLogModel", back_populates="product", cascade="all, delete-orphan"
    )

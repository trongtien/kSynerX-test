from datetime import datetime

from core.database import BaseSchema
from sqlalchemy import Boolean, Column, DateTime, Numeric, String
from sqlalchemy.orm import relationship


class ProductModel(BaseSchema):
    __tablename__ = "products"
    sku = Column(String(100), primary_key=True, index=True)
    parner_sku = Column(
        String(100),
    )
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    checksum_hash = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True)

    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    changes = relationship(
        "ProductAuditLogModel", back_populates="product", cascade="all, delete-orphan"
    )

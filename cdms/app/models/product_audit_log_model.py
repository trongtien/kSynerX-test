from datetime import datetime

from core.database import BaseSchema
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class ProductAuditLogModel(BaseSchema):
    __tablename__ = "product_audit_log"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sku = Column(
        String(100),
        ForeignKey("products.sku", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    change_type = Column(String(20), nullable=False)
    details = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("ProductModel", back_populates="changes")

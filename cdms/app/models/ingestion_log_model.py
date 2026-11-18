from datetime import datetime

from core.database import BaseSchema
from sqlalchemy import Column, DateTime, Integer, String


class IngestionLogModel(BaseSchema):
    __tablename__ = "ingestion_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_type = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False)
    total_records = Column(Integer, default=0)
    created_count = Column(Integer, default=0)
    updated_count = Column(Integer, default=0)
    skipped_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

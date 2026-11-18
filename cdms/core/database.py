from typing import Annotated

from core.config import cdms_setting
from core.logger import logger
from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

engine = create_engine(
    url=cdms_setting.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


class BaseSchema(DeclarativeBase):
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseProvider:
    @staticmethod
    def get_database():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def check_database_connection():
        logger.info("Connecting to database")
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1")).scalar()
            logger.info("Database connection success")
        except Exception as e:
            logger.error(f"Database connection failed\n --> {e}")
            raise

    @staticmethod
    def shutdown_database():
        logger.info("Shutting down database")
        engine.dispose()
        logger.info("Database shutdown success")


DatabaseSession = Annotated[Session, Depends(DatabaseProvider.get_database)]

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class CDMSSetting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    SERVICE_NAME: str = "CDMS"
    SERVICE_VERSION: str = "0.0.1"

    SERVICE_HOST: str = "localhost"
    SERVICE_PORT: int = 3000

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_DB_NAME: str
    DATABASE_DB_USERNAME: str
    DATABASE_DB_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DATABASE_DB_USERNAME}:{self.DATABASE_DB_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_DB_NAME}"


cdms_setting = CDMSSetting()

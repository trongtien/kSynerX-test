import os
from dataclasses import dataclass


def _env_int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _env_float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


@dataclass(frozen=True, slots=True)
class Settings:
    webhook_url: str
    interval_seconds: float
    initial_products: int
    initial_batch_size: int
    create_per_tick: int
    update_per_tick: int
    noop_per_tick: int
    duplicate_rate: float
    max_retries: int
    request_timeout: float
    seed: int


def load_setting() -> Settings:
    return Settings(
        webhook_url=os.getenv(
            "CDMS_WEBHOOK_URL", "http://localhost:3000/webhook/products"
        ),
        interval_seconds=_env_float("INTERVAL_SECONDS", 5),
        initial_products=_env_int("INITIAL_PRODUCTS", 100),
        initial_batch_size=_env_int("INITIAL_BATCH_SIZE", 100),
        create_per_tick=_env_int("CREATE_PER_TICK", 2),
        update_per_tick=_env_int("UPDATE_PER_TICK", 5),
        noop_per_tick=_env_int("NOOP_PER_TICK", 3),
        duplicate_rate=_env_float("DUPLICATE_RATE", 0.1),
        max_retries=_env_int("MAX_RETRIES", 5),
        request_timeout=_env_float("REQUEST_TIMEOUT", 10),
        seed=_env_int("SEED", 42),
    )

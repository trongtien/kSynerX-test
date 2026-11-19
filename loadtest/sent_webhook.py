import logging
import time
from typing import Any

import requests

from loadtest.product import Product, ProductFaker
from loadtest.setting import Settings

logger = logging.getLogger(__name__)

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class SentWebhook:
    def __init__(self, setting: Settings, faker: ProductFaker) -> None:
        self.max_bath_size = 5000
        self.setting = setting
        self.faker = faker
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def send_create(self, total: int, batch_size: int | None = None) -> int:
        size = min(batch_size or self.setting.initial_batch_size, self.max_bath_size)
        sent = 0
        while sent < total:
            count = min(size, total - sent)
            products = [self.faker.new_product() for _ in range(count)]
            self._post(products)
            sent += count
            logger.info("Created %d/%d products", sent, total)
        return sent

    def _post(self, products: list[Product]) -> Any:
        payload = {"products": products}
        for attempt in range(1, self.setting.max_retries + 1):
            try:
                response = self.session.post(
                    self.setting.webhook_url,
                    json=payload,
                    timeout=self.setting.request_timeout,
                )
            except requests.RequestException as e:
                error: str = str(e)
            else:
                if response.ok:
                    return response.json()
                if response.status_code not in RETRYABLE_STATUS:
                    # 4xx (e.g. 422 validation) will not succeed on retry.
                    raise RuntimeError(
                        f"Webhook rejected batch: {response.status_code} {response.text}"
                    )
                error = f"{response.status_code} {response.text}"

            if attempt == self.setting.max_retries:
                raise RuntimeError(f"Webhook failed after {attempt} attempts: {error}")
            delay = min(2 ** (attempt - 1), 30)
            logger.warning(
                "Attempt %d/%d failed (%s), retrying in %ds",
                attempt,
                self.setting.max_retries,
                error,
                delay,
            )
            time.sleep(delay)
        return None

    def close(self) -> None:
        self.session.close()

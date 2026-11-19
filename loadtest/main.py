import logging

from loadtest.product import ProductFaker
from loadtest.sent_webhook import SentWebhook
from loadtest.setting import load_setting


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    setting = load_setting()
    products = ProductFaker(setting.seed)
    webhook = SentWebhook(setting, products)
    try:
        webhook.send_create(setting.initial_products)
    finally:
        webhook.close()


if __name__ == "__main__":
    main()

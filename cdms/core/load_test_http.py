import httpx
from core.config import cdms_setting
from core.logger import logger
from core.path_request import FAKE_PRODUCT_VIETFULL


class LoadTestHttp:
    def __init__(self):
        self.load_test_client = httpx.Client(base_url=cdms_setting.LOAD_TEST_URL)

    def close(self) -> None:
        self.load_test_client.close()

    def exec(self, page_index: int, page_size: int):
        params = {"PageIndex": page_index, "PageSize": page_size}
        try:
            response = self.load_test_client.get(FAKE_PRODUCT_VIETFULL, params=params)
            data = response.json()
            return data
        except httpx.TransportError as e:
            msg = f"cannot reach Vietful ({type(e).__name__})"
            logger.info(f"[ERROR] - Load test calling prodcut error \n --> {msg}")

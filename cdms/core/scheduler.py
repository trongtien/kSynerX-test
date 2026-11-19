import asyncio
import contextlib

from app.services.product_pull_service import ProductPullService
from core.logger import logger


class ProductPullScheduler:
    """
    -> Run ProductPullService.run_pull_product every `interval_seconds`
    -> The pull is blocking (httpx sync + SQLAlchemy sync) so it runs in a
       worker thread to keep the FastAPI event loop free
    -> One failed run is logged and never stops the next run
    """

    def __init__(self, pull_service: ProductPullService, interval_seconds: int):
        self.pull_service = pull_service
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if self._task is not None:
            return
        logger.info(f"Start pull product scheduler (every {self.interval_seconds}s)")
        self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
        self._task = None
        logger.info("Pull product scheduler stopped")

    async def _loop(self) -> None:
        while True:
            await self._run_once()
            await asyncio.sleep(self.interval_seconds)

    async def _run_once(self) -> None:
        try:
            summary = await asyncio.to_thread(self.pull_service.run_pull_product)
            logger.info(f"Pull product done -> {summary}")
        except OSError as e:
            logger.error(f"Pull product failed \n --> {e}")

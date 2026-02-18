import logging
from typing import Any

from litestar.di import Provide
from litestar.stores.redis import RedisStore
from litestar.stores.registry import StoreRegistry

from config import settings
from sender import EmailSender

logger = logging.getLogger(__name__)


def create_stores() -> StoreRegistry:
    """
    Create store registry with optional Redis/DragonflyDB support.
    Falls back to memory store if Redis is unavailable.
    """
    stores: dict[str, Any] = {}

    if not settings.security.redis_url:
        return StoreRegistry()
    
    try:
        redis_store = RedisStore.with_client(url=settings.security.redis_url)
        stores["rate_limit"] = redis_store
        logger.info(
            "Rate limiting configured with Redis/DragonflyDB store",
            extra={"redis_url": settings.security.redis_url.split("@")[-1]},
        )
    except Exception as e:
        logger.warning(
            "Failed to connect to Redis/DragonflyDB, falling back to memory store",
            extra={"error": str(e), "error_type": type(e).__name__},
        )

    return StoreRegistry(stores) if stores else StoreRegistry()


DEPENDENCIES: dict[str, Provide] = {
    "email_sender": Provide(EmailSender, sync_to_thread=False),
}

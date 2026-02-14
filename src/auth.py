"""API Key authentication middleware using Litestar's AbstractAuthenticationMiddleware."""

import logging
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.authentication import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from config import settings

logger = logging.getLogger(__name__)


class APIKeyAuthMiddleware(AbstractAuthenticationMiddleware):
    """Middleware to authenticate requests using X-API-KEY header."""

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        """Validate API key from request headers.

        Args:
            connection: The ASGI connection object containing request data.

        Returns:
            AuthenticationResult with authenticated user data.

        Raises:
            NotAuthorizedException: If API key is missing or invalid.
        """
        api_key = connection.headers.get("X-API-KEY")

        if not api_key:
            logger.warning(
                "Authentication failed: Missing X-API-KEY header from %s",
                connection.client.host if connection.client else "unknown",
            )
            raise NotAuthorizedException(detail="Missing X-API-KEY header")

        if api_key != settings.security.api_key:
            logger.warning(
                "Authentication failed: Invalid API key from %s",
                connection.client.host if connection.client else "unknown",
            )
            raise NotAuthorizedException(detail="Invalid API key")

        logger.info(
            "Authentication successful from %s",
            connection.client.host if connection.client else "unknown",
        )

        return AuthenticationResult(user={"authenticated": True}, auth=api_key)

import warnings

# Suppress Pydantic V1 compatibility warning with Python 3.14
warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
)

import logging
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin, SwaggerRenderPlugin
from litestar.openapi.spec import License

from auth import APIKeyAuthMiddleware
from config import settings
from controllers import NotificationsRouter, HealthController
from register_deps import DEPENDENCIES, create_stores

logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

cors_config = CORSConfig(
    allow_origins=settings.security.cors_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-KEY", "X-CSRF-Token"],
    allow_credentials=True,
    max_age=600,
)

rate_limit_config = RateLimitConfig(
    rate_limit=(
        settings.security.rate_limit_window,
        settings.security.rate_limit_requests,
    ),
    exclude=[r"^/$", r"^/schema/?.*"],
    identifier_for_request=lambda request: (
        request.client.host if request.client else "unknown"
    ),
    store="rate_limit",  # Will use Redis/DragonflyDB if configured, otherwise memory
)

csrf_config = (
    CSRFConfig(
        secret=settings.security.api_key,
        cookie_httponly=True,
        cookie_secure=not settings.debug,
    )
    if settings.security.enable_csrf
    else None
)

app = Litestar(
    debug=settings.debug,
    dependencies=DEPENDENCIES,
    stores=create_stores(),
    route_handlers=[HealthController, NotificationsRouter],
    middleware=[APIKeyAuthMiddleware, rate_limit_config.middleware],
    cors_config=cors_config,
    csrf_config=csrf_config,
    openapi_config=OpenAPIConfig(
        title="Zozbit Notifications API",
        version="1.0.0",
        description="API for sending email notifications with security features: API key authentication, rate limiting, and CORS protection.",
        license=License(name="MIT", url="https://opensource.org/licenses/MIT"),
        path="/",
        render_plugins=[
            SwaggerRenderPlugin(),
            RedocRenderPlugin(),
        ],
        security=[{"apiKey": []}],
    ),
)

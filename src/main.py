import warnings

# Suppress Pydantic V1 compatibility warning with Python 3.14
warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
)

from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin, SwaggerRenderPlugin
from litestar.openapi.spec import License


from config import settings
from register_deps import DEPENDENCIES
from controllers import NotificationsRouter

app = Litestar(
    debug=settings.debug,
    dependencies=DEPENDENCIES,
    route_handlers=[NotificationsRouter],
    openapi_config=OpenAPIConfig(
        title="Zozbit Notifications API",
        version="1.0.0",
        description="API for sending email notifications",
        license=License(name="MIT", url="https://opensource.org/licenses/MIT"),
        path="/",
        render_plugins=[
            SwaggerRenderPlugin(),
            RedocRenderPlugin(),
        ],
    ),
)

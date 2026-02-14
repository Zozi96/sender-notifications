from typing import Annotated

from litestar import Controller, Response, get, post, status_codes
from litestar.background_tasks import BackgroundTask
from litestar.contrib.pydantic import PydanticDTO
from litestar.openapi.spec import Example
from litestar.openapi.datastructures import ResponseSpec
from litestar.params import Body
from litestar.connection import ASGIConnection

from schemas import EmailInput, SuccessResponse, HealthResponse
from sender import ISender


class HealthController(Controller):
    path: str = "/health"
    tags = ["Health"]

    @get(
        summary="Health check endpoint",
        description=(
            "Returns the service health status. "
            "This endpoint does not require authentication and can be used to: "
            "1) Verify the service is running, "
            "2) Obtain CSRF cookie for POST requests (if CSRF protection is enabled).\n\n"
            "**Frontend Integration:**\n"
            "Call this endpoint first to receive the CSRF cookie, then include it automatically "
            "in subsequent POST requests using `credentials: 'include'`."
        ),
        return_dto=PydanticDTO[HealthResponse],
        status_code=status_codes.HTTP_200_OK,
        response_description="Service is healthy",
        exclude_from_auth=True,
        responses={
            status_codes.HTTP_200_OK: ResponseSpec(
                data_container=PydanticDTO[HealthResponse],
                media_type="application/json",
                description="Service health status",
                examples=[Example(summary="Healthy", value={"status": "healthy"})],
            ),
        },
    )
    async def health_check(self, request: ASGIConnection) -> Response[HealthResponse]:
        return Response(
            content=HealthResponse(status="healthy"),
            status_code=status_codes.HTTP_200_OK,
        )


class NotificationsRouter(Controller):
    path: str = "/notifications"
    tags = ["Notifications"]

    @post(
        path="/send-email",
        summary="Send an email notification",
        description=(
            "Sends a styled HTML email notification with embedded logo using the notification template. "
            "The email is sent asynchronously in the background, so this endpoint returns immediately. "
            "The notification includes customizable headline, body, badge, call-to-action button, and footer.\n\n"
            "**Possible Responses:**\n"
            "- `201`: Email queued successfully\n"
            "- `400`: Validation error (missing required fields, invalid length, etc.)\n"
            "- `422`: Invalid JSON in request body\n"
            "- `500`: Internal server error"
        ),
        return_dto=PydanticDTO[SuccessResponse],
        status_code=status_codes.HTTP_201_CREATED,
        response_description="Email queued successfully and will be sent in the background",
        raises=[],
        responses={
            status_codes.HTTP_201_CREATED: ResponseSpec(
                data_container=PydanticDTO[SuccessResponse],
                media_type="application/json",
                description="Email queued successfully",
                examples=[
                    Example(
                        summary="Successful Response",
                        value={"message": "Email sent successfully"},
                    )
                ],
            ),
        },
    )
    async def send_email(
        self,
        data: Annotated[
            EmailInput,
            Body(
                title="Email notification data",
                description="Complete email notification payload with subject and template variables",
            ),
        ],
        email_sender: ISender[EmailInput],
    ) -> Response[SuccessResponse]:
        return Response(
            content=SuccessResponse(message="Email sent successfully"),
            background=BackgroundTask(email_sender.send, data),
            status_code=status_codes.HTTP_201_CREATED,
        )

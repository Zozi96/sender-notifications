from typing import Annotated

from litestar import Controller, Response, post, status_codes
from litestar.background_tasks import BackgroundTask
from litestar.contrib.pydantic import PydanticDTO
from litestar.openapi.spec import Example
from litestar.openapi.datastructures import ResponseSpec
from litestar.params import Body

from schemas import EmailInput, SuccessResponse
from sender import ISender


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
                examples=[Example(summary="Successful Response", value={"message": "Email sent successfully"})],
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

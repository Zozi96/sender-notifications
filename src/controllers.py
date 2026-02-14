from typing import Annotated

from litestar import Controller, Response, post, status_codes
from litestar.background_tasks import BackgroundTask
from litestar.contrib.pydantic import PydanticDTO
from litestar.params import Body
from litestar.openapi.spec import Example

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
            "The notification includes customizable headline, body, badge, call-to-action button, and footer."
        ),
        return_dto=PydanticDTO[SuccessResponse],
        status_code=status_codes.HTTP_201_CREATED,
        response_description="Email queued successfully and will be sent in the background",
        raises=[],
    )
    async def send_email(
        self,
        data: Annotated[
            EmailInput,
            Body(
                title="Email notification data",
                description="Complete email notification payload with subject and template variables",
                examples=[
                    Example(
                        summary="Welcome email",
                        description="Example of a welcome notification email",
                        value={
                            "subject": "Welcome to Zozbit!",
                            "templateVariables": {
                                "headline": "Your account is ready",
                                "body": "We're excited to have you on board. Your account has been successfully created and verified.",
                                "badge": "Welcome",
                                "actionUrl": "https://app.zozbit.com/dashboard",
                                "actionLabel": "Go to Dashboard",
                                "footerNote": "If you didn't create this account, please contact our support team.",
                            },
                            "previewText": "Your account has been successfully created and verified.",
                        },
                    ),
                    Example(
                        summary="Security alert",
                        description="Example of a security notification",
                        value={
                            "subject": "Security Alert - Unusual Activity Detected",
                            "templateVariables": {
                                "headline": "Unusual login detected",
                                "body": "We detected a login to your account from a new device or location. If this was you, you can safely ignore this message.",
                                "badge": "Security",
                                "actionUrl": "https://app.zozbit.com/security",
                                "actionLabel": "Review Activity",
                                "footerNote": "If this wasn't you, please secure your account immediately.",
                            },
                            "previewText": "We detected a login from a new device or location.",
                        },
                    ),
                    Example(
                        summary="Simple notification without button",
                        description="Minimal notification without call-to-action button",
                        value={
                            "subject": "Your report is ready",
                            "templateVariables": {
                                "headline": "Monthly report generated",
                                "body": "Your monthly analytics report has been generated and is available for download in your dashboard.",
                                "badge": "Report",
                            },
                            "previewText": "Your monthly analytics report is ready.",
                        },
                    ),
                ],
            ),
        ],
        email_sender: ISender[EmailInput],
    ) -> Response[SuccessResponse]:
        return Response(
            content=SuccessResponse(message="Email sent successfully"),
            background=BackgroundTask(email_sender.send, data),
            status_code=status_codes.HTTP_201_CREATED,
        )

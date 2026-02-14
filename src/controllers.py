from typing import Annotated

from litestar import Controller, Response, post
from litestar.background_tasks import BackgroundTask
from litestar.contrib.pydantic import PydanticDTO
from litestar.params import Body

from schemas import EmailInput, SuccessResponse
from sender import ISender


class NotificationsRouter(Controller):
    path: str = "/notifications"
    tags = ["Notifications"]

    @post(
        path="/send-email",
        summary="Send an email notification",
        description="Send an email notification to a specified recipient.",
        return_dto=PydanticDTO[SuccessResponse],
    )
    async def send_email(
        self, data: Annotated[EmailInput, Body()], email_sender: ISender[EmailInput]
    ) -> Response[SuccessResponse]:
        return Response(
            content=SuccessResponse(message="Email sent successfully"),
            background=BackgroundTask(email_sender.send, data),
        )

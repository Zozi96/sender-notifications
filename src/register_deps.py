from litestar.di import Provide

from sender import EmailSender


DEPENDENCIES: dict[str, Provide] = {
    "email_sender": Provide(EmailSender, sync_to_thread=False),
}

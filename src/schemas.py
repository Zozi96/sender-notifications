from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class NotificationTemplateVariables(CamelModel):
    """Variables for the notification email template."""

    headline: str = Field(
        ...,
        description="Main headline displayed prominently in the email",
        examples=["Welcome to Zozbit!", "Your account is ready", "Action required"],
        min_length=1,
        max_length=200,
    )
    body: str = Field(
        ...,
        description="Main body text content of the notification",
        examples=[
            "Your account has been successfully verified.",
            "We've detected unusual activity on your account.",
        ],
        min_length=1,
    )
    badge: str = Field(
        default="Notification",
        description="Badge label displayed at the top of the email card",
        examples=["Alert", "Update", "Reminder", "Security"],
        max_length=50,
    )
    action_url: str | None = Field(
        default=None,
        description="URL for the call-to-action button. If provided, a button will be displayed",
        examples=["https://app.zozbit.com/dashboard", "https://app.zozbit.com/verify"],
    )
    action_label: str = Field(
        default="View Details",
        description="Text label for the call-to-action button",
        examples=["Go to Dashboard", "Verify Now", "Learn More", "Get Started"],
        max_length=50,
    )
    footer_note: str | None = Field(
        default=None,
        description="Optional footer note or disclaimer text",
        examples=[
            "If you didn't request this, please ignore this email.",
            "This is an automated message, please do not reply.",
        ],
        max_length=500,
    )


class EmailInput(CamelModel):
    """Input schema for sending email notifications."""

    subject: str = Field(
        ...,
        description="Email subject line",
        examples=["Welcome to Zozbit", "Security Alert", "Account Verification"],
        min_length=1,
        max_length=200,
    )
    template_variables: NotificationTemplateVariables = Field(
        ...,
        description="Variables to populate the notification template",
    )
    preview_text: str | None = Field(
        default=None,
        description="Preview text for email clients (plain text fallback)",
        examples=["Your account has been verified successfully"],
        max_length=200,
    )


class SuccessResponse(CamelModel):
    message: str

# Sender Notifications API

A secure, production-ready email notification API built with Litestar, designed for sending styled HTML email notifications with comprehensive security features.

## Features

- 🔐 **API Key Authentication** - Secure endpoint access with X-API-KEY header
- 🛡️ **CSRF Protection** - Built-in CSRF token validation
- 🚦 **IP-Based Rate Limiting** - Per-IP rate limiting to prevent abuse (10 requests/minute default)
- 🌐 **CORS Support** - Configurable Cross-Origin Resource Sharing
- 📧 **HTML Email Templates** - Beautiful, responsive email templates with Jinja2
- 🎨 **Customizable Notifications** - Support for headlines, body text, badges, CTA buttons, and footer notes
- 🔒 **XSS Protection** - Automatic HTML sanitization with bleach
- 📊 **Structured Logging** - Detailed contextual logging for debugging and monitoring
- 🐋 **Docker Support** - Production-ready containerization
- 📝 **OpenAPI/Swagger** - Interactive API documentation

## Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer (recommended)
- SMTP server credentials (e.g., Gmail, SendGrid, AWS SES)

## Installation

### Using uv (Recommended)

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/Zozi96/sender-notifications.git
cd sender-notifications
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` with your configuration (see Configuration section below)

5. Install dependencies (uv will handle this automatically when running the app)

## Configuration

Configure the application by editing the `.env` file:

### Required Environment Variables

```bash
# Email Configuration (REQUIRED)
EMAIL_SENDER=noreply@yourdomain.com
EMAIL_RECIPIENT=recipient@example.com

# SMTP Settings (REQUIRED)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
```

### Security Settings (REQUIRED for Production)

```bash
# Generate a strong API key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
API_KEY=your-secure-random-key-here

# CORS Configuration - JSON array of allowed origins
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=minute

# CSRF Protection (disable for API-only usage)
ENABLE_CSRF=false
```

### Optional Settings

```bash
# Application Settings
DEBUG=false
```

## Local Development

Run the application locally with auto-reload:

```bash
uv run --directory src -- litestar run --app main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/schema/swagger
- **ReDoc**: http://localhost:8000/schema/redoc
- **Health Check**: http://localhost:8000/health

## API Documentation

### Authentication

All endpoints (except `/health` and `/schema/*`) require authentication via the `X-API-KEY` header:

```bash
X-API-KEY: your-api-key-here
```

### Endpoints

#### Health Check

```http
GET /health
```

Returns the service health status. No authentication required.

**Response:**
```json
{
  "status": "healthy"
}
```

#### Send Email Notification

```http
POST /notifications/send-email
```

Sends a styled HTML email notification.

**Headers:**
```
Content-Type: application/json
X-API-KEY: your-api-key-here
```

**Request Body:**
```json
{
  "subject": "Welcome to Zozbit!",
  "templateVariables": {
    "headline": "Your Account is Ready",
    "body": "Thank you for signing up. Your account has been successfully created and verified.",
    "badge": "Welcome",
    "actionUrl": "https://app.zozbit.com/dashboard",
    "actionLabel": "Go to Dashboard",
    "footerNote": "If you didn't create this account, please ignore this email."
  },
  "previewText": "Your account has been successfully created"
}
```

**Response (201 Created):**
```json
{
  "message": "Email sent successfully"
}
```

### Example Usage

#### Using curl:

```bash
curl -X POST http://localhost:8000/notifications/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-api-key-here" \
  -d '{
    "subject": "Security Alert",
    "templateVariables": {
      "headline": "Unusual Activity Detected",
      "body": "We detected a login from a new device. If this was you, no action is needed.",
      "badge": "Security",
      "actionUrl": "https://app.zozbit.com/security",
      "actionLabel": "Review Activity"
    }
  }'
```

#### Using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/notifications/send-email",
    headers={
        "Content-Type": "application/json",
        "X-API-KEY": "your-api-key-here"
    },
    json={
        "subject": "Account Verification",
        "templateVariables": {
            "headline": "Verify Your Email",
            "body": "Please click the button below to verify your email address.",
            "badge": "Verification",
            "actionUrl": "https://app.zozbit.com/verify/abc123",
            "actionLabel": "Verify Now",
            "footerNote": "This link expires in 24 hours."
        },
        "previewText": "Click to verify your email address"
    }
)

print(response.status_code)
print(response.json())
```

#### Using JavaScript fetch:

```javascript
const response = await fetch('http://localhost:8000/notifications/send-email', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-KEY': 'your-api-key-here'
  },
  body: JSON.stringify({
    subject: 'Password Reset',
    templateVariables: {
      headline: 'Reset Your Password',
      body: 'Click the button below to reset your password. This link is valid for 1 hour.',
      badge: 'Security',
      actionUrl: 'https://app.zozbit.com/reset/xyz789',
      actionLabel: 'Reset Password',
      footerNote: 'If you didn\'t request this, please ignore this email.'
    }
  })
});

const data = await response.json();
console.log(data);
```

## Docker Deployment

### Build and Run with Docker

1. Build the Docker image:
```bash
docker build -t sender-notifications:latest .
```

2. Run the container:
```bash
docker run -d \
  --name sender-notifications \
  -p 8000:8000 \
  --env-file .env \
  sender-notifications:latest
```

### Using Docker Compose

1. Create or edit `.env` file with your configuration

2. Start the service:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the service:
```bash
docker-compose down
```

### Environment Variables in Docker

You can pass environment variables directly:

```bash
docker run -d \
  --name sender-notifications \
  -p 8000:8000 \
  -e API_KEY=your-secure-key \
  -e EMAIL_SENDER=noreply@yourdomain.com \
  -e EMAIL_RECIPIENT=admin@yourdomain.com \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -e SMTP_USE_TLS=true \
  -e CORS_ORIGINS='["https://yourdomain.com"]' \
  sender-notifications:latest
```

## Security Best Practices

### API Key Security

1. **Generate Strong Keys**: Use cryptographically secure random keys
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Never Commit Keys**: Keep `.env` files out of version control
   - Already configured in `.gitignore`
   - Use environment variables in production

3. **Rotate Keys Regularly**: Change API keys periodically

4. **Use Different Keys**: Use separate keys for development and production

### SMTP Security

1. **Use App Passwords**: For Gmail, use app-specific passwords
2. **Enable TLS**: Always use `SMTP_USE_TLS=true`
3. **Secure Credentials**: Never log or expose SMTP credentials

### CORS Configuration

1. **Specific Origins**: Never use wildcard (`*`) in production
   ```bash
   CORS_ORIGINS=["https://yourdomain.com"]
   ```

2. **Multiple Origins**: Use JSON array format
   ```bash
   CORS_ORIGINS=["https://app.yourdomain.com", "https://admin.yourdomain.com"]
   ```

### Rate Limiting

- Default: 10 requests per minute per IP
- Adjust based on your needs:
  ```bash
  RATE_LIMIT_REQUESTS=20
  RATE_LIMIT_WINDOW=minute  # second, minute, hour, day
  ```

### CSRF Protection

- Enable for browser-based clients:
  ```bash
  ENABLE_CSRF=true
  ```
- Disable for API-only usage:
  ```bash
  ENABLE_CSRF=false
  ```

### Input Validation

All user inputs are automatically sanitized:
- HTML tags stripped from text fields
- Email addresses validated at configuration time
- String length limits enforced
- XSS protection via bleach library

## Project Structure

```
sender-notifications/
├── src/
│   ├── main.py              # Application entry point, middleware configuration
│   ├── config.py            # Configuration and settings with email validation
│   ├── auth.py              # API key authentication middleware
│   ├── controllers.py       # API route handlers
│   ├── sender.py            # Email sending logic with error handling
│   ├── schemas.py           # Pydantic models for request/response
│   ├── register_deps.py     # Dependency injection setup
│   ├── templates/           # Jinja2 email templates
│   │   └── notification.html
│   └── static/              # Static assets (logos, images)
│       └── zozbit.png
├── .env.example             # Example environment configuration
├── .dockerignore            # Docker build exclusions
├── Dockerfile               # Production Docker image
├── docker-compose.yml       # Docker Compose configuration
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Dependency lock file
└── README.md                # This file
```

## Logging

The application uses structured logging with contextual information:

### Success Logs
```
INFO - Email sent successfully
  recipient: user@example.com
  sender: noreply@yourdomain.com
  subject: Welcome Email
```

### Error Logs
```
ERROR - SMTP error while sending email
  recipient: user@example.com
  sender: noreply@yourdomain.com
  subject: Welcome Email
  error_type: SMTPAuthenticationError
  error_message: Authentication failed
```

### Template Warnings
```
WARNING - Template not found, using fallback HTML
  template_name: notification.html
  error_type: TemplateNotFound
```

## Troubleshooting

### Common Issues

**1. SMTP Authentication Failed**
- Verify SMTP credentials in `.env`
- For Gmail, use app-specific password (not account password)
- Check if 2FA is enabled and create an app password

**2. Rate Limit Exceeded**
```json
{
  "status_code": 429,
  "detail": "Rate limit exceeded"
}
```
- Wait for the rate limit window to reset
- Increase `RATE_LIMIT_REQUESTS` if needed

**3. Invalid Email Configuration**
```
ValidationError: email_sender
```
- Ensure EMAIL_SENDER and EMAIL_RECIPIENT are valid email addresses
- Check for typos or formatting issues

**4. CORS Errors**
- Add your frontend domain to `CORS_ORIGINS`
- Ensure JSON array format: `["https://yourdomain.com"]`

**5. Template Not Found**
- The app will fall back to basic HTML if templates are missing
- Check that `src/templates/notification.html` exists

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [https://github.com/Zozi96/sender-notifications/issues](https://github.com/Zozi96/sender-notifications/issues)
- Documentation: This README

## Acknowledgments

Built with:
- [Litestar](https://litestar.dev/) - Fast, flexible ASGI framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [aiosmtplib](https://aiosmtplib.readthedocs.io/) - Async SMTP client
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

# Use Python 3.14+ base image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/

# Expose port 8000 (default Litestar port)
EXPOSE 8000

# Run the application in production mode
CMD ["uv", "run", "--directory", "src", "--", "litestar", "run", "--app", "main:app", "--host", "0.0.0.0", "--port", "8000"]

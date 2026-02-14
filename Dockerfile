# Use a specific version for the builder to ensure reproducibility
FROM ghcr.io/astral-sh/uv:0.5.11 AS uv

# Base image
FROM python:3.14-slim

# Security: Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Optimization: Bytecode compilation variables
# We WANT bytecode compiled during build for speed, but not written at runtime
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install uv binary
COPY --from=uv /uv /usr/local/bin/uv

# 1. Dependency Layer
# Copy only dependency definitions first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies WITHOUT installing the project itself.
# This ensures this layer is cached unless dependencies change.
RUN uv sync --frozen --no-dev --no-install-project

# 2. Application Layer
COPY src/ ./src/

# Install the project itself (if it's a package) and sync environment
RUN uv sync --frozen --no-dev

# Security: Change ownership to non-root user
# Note: We do this after install so the user can access the files
RUN chown -R appuser:appuser /app

# Optimization: Add venv to PATH
# This removes the need for 'uv run' prefix and 'source .venv/bin/activate'
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

EXPOSE 8000

# Run directly without the uv wrapper
# Host 0.0.0.0 is correct for Docker networking
CMD ["litestar", "run", "--app", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

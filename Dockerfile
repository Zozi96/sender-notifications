FROM ghcr.io/astral-sh/uv:0.5.11 AS uv

FROM python:3.14-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=uv /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./

RUN uv sync --frozen --no-dev

RUN chown -R appuser:appuser /app

ENV PATH="/app/.venv/bin:$PATH"

ARG PORT=8000
ENV PORT=${PORT}

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

USER appuser

EXPOSE ${PORT}

ENTRYPOINT ["./entrypoint.sh"]

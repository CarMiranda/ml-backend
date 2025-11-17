ARG DEBIAN_FRONTEND=noninteractive
ARG COMMIT="unknown"

FROM python:3.12-slim AS builder

  RUN apt-get update && \
      apt-get install --no-install-recommends \
      -y git tzdata && \
      rm -rf /var/lib/apt/lists/*

  COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
  ENV UV_COMPILE_BYTECODE=1
  ENV UV_LINK_MODE=copy

  WORKDIR /app

# Install dependencies
  RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=source=uv.lock,target=uv.lock,type=bind \
    --mount=source=pyproject.toml,target=pyproject.toml,type=bind \
    uv sync --locked --no-install-project --no-editable --no-dev

  COPY uv.lock pyproject.toml README.md /app/
  COPY src /app/src

  RUN --mount=source=.git,target=.git,type=bind \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev

###
FROM python:3.12-slim

  RUN useradd -m -s /bin/sh -u 1001 app
  USER app
  WORKDIR /app

  COPY --from=builder --chown=app:app /app/.venv /app/.venv

  EXPOSE 8000
  ENV COMMIT=$COMMIT

# COPY health.py .
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD uv run health.py || exit 1

  COPY .prod.env .env

  CMD ["/app/.venv/bin/ml-backend"]

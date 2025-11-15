# Builder stage
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /app

COPY uv.lock pyproject.toml README.md ./
COPY app ./app/

RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 \
    uv pip install --system --no-cache .

# Runner stage
FROM python:3.14-slim AS runner

WORKDIR /ntlcli/

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /ntlcli/
COPY datasets.yaml ./

ENV PYTHONPATH=/ntlcli \
    PYTHONUNBUFFERED=1

CMD ["ntlcli", "ingest", "-zygf", "--use-polars"]
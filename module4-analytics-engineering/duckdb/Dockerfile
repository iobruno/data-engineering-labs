# Builder stage
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

WORKDIR /app

COPY uv.lock pyproject.toml README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 \
    uv pip install --system --no-cache .

ADD analyses                                        /dbt/analyses
ADD macros                                          /dbt/macros
ADD models                                          /dbt/models
ADD seeds                                           /dbt/seeds
ADD tests                                           /dbt/tests
ADD dbt_project.yml package-lock.yml packages.yml   /dbt/
ADD profiles.tmpl.yml                               /dbt/profiles.yml

# Runner stage
FROM python:3.13-slim AS runner

WORKDIR /dbt/

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /dbt /dbt

ENV DBT_PROFILES_DIR=/dbt/
ENV DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH=
ENV DBT_DUCKDB_TARGET_PATH=/tmp/dbt.duckdb
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp_credentials.json

ENTRYPOINT ["sh", "-c", "dbt deps && dbt build --target prod && cp target/run_results.json target/run_results_backup.json && dbt docs generate --target prod && cp target/run_results_backup.json target/run_results.json"]
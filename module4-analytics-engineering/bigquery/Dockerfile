ARG PYTHON_VERSION=3.14

# Builder stage
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-trixie-slim AS builder

WORKDIR /dbt

ENV UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

COPY pyproject.toml uv.lock         ./
COPY packages.yml package-lock.yml  ./
COPY dbt_project.yml                ./
COPY profiles.tmpl.yml              ./profiles.yml

COPY analyses                       ./analyses
COPY macros                         ./macros
COPY models                         ./models
COPY seeds                          ./seeds
COPY snapshots                      ./snapshots
COPY tests                          ./tests

# --no-install-package: never downloaded, never built. Only reachable from
# BigFrames/Dataproc Python models and to_dataframe(); this project has neither.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev \
        --no-install-project \
        --no-install-package dbt-core-experimental-parser \
        --no-install-package google-cloud-aiplatform \
        --no-install-package google-genai \
        --no-install-package google-cloud-resource-manager \
        --no-install-package nbformat \
        --no-install-package pyarrow \
        --no-install-package pandas \
        --no-install-package numpy \
        --no-install-package pandas-gbq \
        --no-install-package db-dtypes \
        --no-install-package pydata-google-auth

RUN dbt deps


# Runner stage
FROM python:${PYTHON_VERSION}-slim-trixie AS runner

ARG PYTHON_VERSION

WORKDIR /dbt

COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /dbt /dbt

ENV DBT_PROFILES_DIR=/dbt/
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp_credentials.json

# Read by profiles.yml, models/staging/sources.yml and
# macros/resolve_destination_schema.sql. Supply these at `docker run`.
ENV DBT_BIGQUERY_PROJECT=
ENV DBT_BIGQUERY_SOURCE_DATASET=
ENV DBT_BIGQUERY_TARGET_DATASET=
ENV DBT_BIGQUERY_DATASET_LOCATION=

ENTRYPOINT ["sh", "-c", "dbt build --target prod && cp target/run_results.json target/run_results_backup.json && dbt docs generate --target prod && cp target/run_results_backup.json target/run_results.json"]

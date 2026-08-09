# Builder stage
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /dbt

ENV UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    SITE_PACKAGES=/usr/local/lib/python3.14/site-packages

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
        --no-install-package pydata-google-auth \
        # orphaned by the exclusions above — not independent choices
        --no-install-package setuptools \
        --no-install-package websockets \
        --no-install-package oauthlib \
        --no-install-package requests-oauthlib \
        --no-install-package google-auth-oauthlib \
        --no-install-package traitlets \
        --no-install-package jupyter-core

# Running the CLI also caches its imports' bytecode into site-packages — clean that up too.
RUN dbt deps \
    && rm -rf logs .user.yml \
    && rm -rf ${SITE_PACKAGES}/pip ${SITE_PACKAGES}/pip-*.dist-info \
    && find ${SITE_PACKAGES} -name '__pycache__' -type d -prune -exec rm -rf {} +


# Runner stage
FROM python:3.14-slim-trixie AS runner

WORKDIR /dbt

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin/dbt /usr/local/bin/dbt
COPY --from=builder /dbt /dbt

ENV DBT_PROFILES_DIR=/dbt/
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp_credentials.json

# Read by profiles.yml, models/staging/sources.yml and macros/resolve_destination_schema.sql
ENV DBT_BIGQUERY_PROJECT=
ENV DBT_BIGQUERY_SOURCE_DATASET=
ENV DBT_BIGQUERY_TARGET_DATASET=
ENV DBT_BIGQUERY_DATASET_LOCATION=

ENTRYPOINT dbt build --target prod \
    && cp target/run_results.json target/run_results.json.bak \
    && dbt docs generate --target prod \
    && cp target/run_results.json.bak target/run_results.json

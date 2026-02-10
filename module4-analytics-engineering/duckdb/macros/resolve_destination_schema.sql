{% macro resolve_schema_for(model_type) -%}

    {{- resolve_type(model_type) -}}

{%- endmacro %}


{% macro resolve_type(model_type='staging') -%}

    {%- set target_env_var = 'DBT_DUCKDB_TARGET_SCHEMA'  -%}
    {%- set staging_env_var = 'DBT_DUCKDB_STAGING_SCHEMA' -%}

    {%- if model_type == 'core' -%} {{- env_var(target_env_var, 'main') -}}
    {%- else -%}                    {{- env_var(staging_env_var, 'main') -}}
    {%- endif -%}

{%- endmacro %}
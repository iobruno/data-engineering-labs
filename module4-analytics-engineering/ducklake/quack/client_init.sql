-- Client-side bootstrap for SQL tools (DataGrip, DBeaver, ...) connecting to
-- the warehouse through their embedded DuckDB JDBC driver. Unlike
-- quack/init.sql (which boots the *server*), this runs on the *client* and
-- attaches out to it, mirroring what profiles.tmpl.yml does for dbt.
--
-- DATA_PATH is deliberately omitted: once the catalog has been created (e.g.
-- by a `dbt build`), DuckLake reads it back from the catalog's own metadata.
-- Only add it back if you're bootstrapping a brand-new, empty catalog --
-- and if so, it must match DBT_DUCKLAKE_DATA_PATH exactly.
INSTALL quack; LOAD quack;
INSTALL ducklake; LOAD ducklake;

CREATE SECRET (TYPE quack, TOKEN 'quack');   -- must match QUACK_TOKEN in compose.yaml

ATTACH 'ducklake:quack:localhost:9494' AS warehouse (
    META_DISABLE_SSL true
);

/* DUCKDB_CONNECTION_INIT_BELOW_MARKER */
USE warehouse;

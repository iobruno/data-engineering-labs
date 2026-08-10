-- Boots the DuckDB catalog server for DuckLake: loads the Quack extension and
-- serves this DuckDB instance over HTTP so dbt (and any other DuckDB client)
-- can ATTACH to it as a DuckLake metadata catalog, instead of opening the
-- database file directly (which only one process could hold at a time).
--
-- This server only holds catalog metadata -- table/schema definitions,
-- snapshots -- not the Parquet data itself. Clients write Parquet straight to
-- DBT_DUCKLAKE_DATA_PATH, so no object-store credentials are needed here.
--
-- Docs: https://duckdb.org/docs/current/quack/overview
INSTALL quack;
LOAD quack;

CALL quack_serve(
    'quack:0.0.0.0:9494',
    token => getenv('QUACK_TOKEN'),
    allow_other_hostname => true,
    disable_ssl => true
);

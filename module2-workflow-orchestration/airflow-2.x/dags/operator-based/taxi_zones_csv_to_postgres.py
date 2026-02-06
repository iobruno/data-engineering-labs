import logging
from pathlib import Path

import pandas as pd
import polars as pl
from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime

logger = logging.getLogger(__name__)


def fetch_dataset(url: str, xcom_id: str, **context: dict):
    logger.info(f"Attempting to fetch dataset from: '{url}'")
    df = pd.read_csv(url, engine="pyarrow")
    logger.info("Dataset sucessfully fetched, serialzing to XCOM's backend...")
    logger.warning("Converting to pd.DataFrame as it's natively supported by Airflow Serde...")
    logger.warning("Implement serde for Feather or Arrow Flight for optimal performance...")
    context["ti"].xcom_push(key=xcom_id, value=df)


def persist_with(conn_string: str, table_name: str, xcom_id: str, **context: dict):
    logger.info("Fetching DataFrame from XCOM backend...")
    obj = context["ti"].xcom_pull(
        task_ids="fetch_taxi_zones_dataset",
        key=xcom_id,
    )
    logger.info("Done! Now preparing to serialize to Postgres...")
    df = pl.from_pandas(
        obj,
        schema_overrides={
            "LocationID": pl.Int32,
            "Borough": pl.Utf8,
            "Zone": pl.Utf8,
            "service_zone": pl.Utf8,
        },
    ).rename({
        "LocationID": "location_id",
        "Borough": "borough",
        "Zone": "zone",
        "service_zone": "service_zone",
    })
    df.write_database(
        table_name=table_name,
        connection=conn_string,
        engine="adbc",
        if_table_exists="replace",
    )
    logger.info("Serialization complete")


with DAG(
    dag_id="op_taxi_zones_csv_to_postgres.py",
    start_date=datetime(2019, 1, 1),
    schedule="@once",
    catchup=False,
    concurrency=1,
    tags=["operator", "polars", "pandas", "postgres"],
):
    dataset_url: str = "{base_url}/download/{dataset}/{filename}".format(
        base_url="https://github.com/DataTalksClub/nyc-tlc-data/releases",
        dataset="misc",
        filename="taxi_zone_lookup.csv",
    )
    xcom_id: str = Path(dataset_url).name

    fetch_dataset = PythonOperator(
        task_id="fetch_taxi_zones_dataset",
        python_callable=fetch_dataset,
        op_kwargs=dict(url=dataset_url, xcom_id=xcom_id),
    )

    persist_to_postgres = PythonOperator(
        task_id="postgres_serialization",
        python_callable=persist_with,
        op_kwargs=dict(
            conn_string="postgres://postgres:postgres@ingest-db:5432/nyc_taxi",
            table_name="zone_lookup",
            xcom_id=xcom_id,
        ),
    )

    fetch_dataset >> persist_to_postgres

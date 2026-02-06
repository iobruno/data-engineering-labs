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
        task_ids="fetch_fhv_dataset",
        key=xcom_id,
    )
    logger.info("Done! Now preparing to serialize to Postgres...")
    df = pl.from_pandas(
        obj,
        schema_overrides={
            "dispatching_base_num": pl.Utf8,
            "pickup_datetime": pl.Datetime,
            "dropOff_datetime": pl.Datetime,
            "PUlocationID": pl.Int32,
            "DOlocationID": pl.Int32,
            "SR_Flag": pl.Int8,
            "Affiliated_base_number": pl.Utf8,
        },
    ).rename({
        "dispatching_base_num": "dispatching_base_num",
        "pickup_datetime": "pickup_datetime",
        "dropOff_datetime": "dropoff_datetime",
        "PUlocationID": "pu_location_id",
        "DOlocationID": "do_location_id",
        "SR_Flag": "sr_flag",
        "Affiliated_base_number": "affiliated_base_number",
    })
    df.write_database(
        table_name=table_name,
        connection=conn_string,
        engine="adbc",
        if_table_exists="append",
    )
    logger.info("Serialization complete")


with DAG(
    dag_id="op_fhv_csv_to_postgres.py",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 12, 1),
    schedule="@monthly",
    catchup=True,
    concurrency=2,
    tags=["operator", "polars", "pandas", "postgres"],
):
    dataset_url: str = "{base_url}/download/{dataset}/{filename}".format(
        base_url="https://github.com/DataTalksClub/nyc-tlc-data/releases",
        dataset="fhv",
        filename="fhv_tripdata_{{ execution_date.strftime('%Y-%m') }}.csv.gz",
    )
    xcom_id: str = Path(dataset_url).name

    fetch_dataset = PythonOperator(
        task_id="fetch_fhv_dataset",
        python_callable=fetch_dataset,
        op_kwargs=dict(url=dataset_url, xcom_id=xcom_id),
    )

    persist_to_postgres = PythonOperator(
        task_id="postgres_serialization",
        python_callable=persist_with,
        op_kwargs=dict(
            conn_string="postgres://postgres:postgres@ingest-db:5432/nyc_taxi",
            table_name="fhv_trips",
            xcom_id=xcom_id,
        ),
    )

    fetch_dataset >> persist_to_postgres

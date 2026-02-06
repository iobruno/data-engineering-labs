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
        task_ids="fetch_green_taxi_dataset",
        key=xcom_id,
    )
    logger.info("Done! Now preparing to serialize to Postgres...")
    df = pl.from_pandas(
        obj,
        schema_overrides={
            "VendorID": pl.Int32,
            "lpep_pickup_datetime": pl.Datetime,
            "lpep_dropoff_datetime": pl.Datetime,
            "passenger_count": pl.Int8,
            "trip_distance": pl.Float64,
            "PULocationID": pl.Int32,
            "DOLocationID": pl.Int32,
            "RatecodeID": pl.Int8,
            "store_and_fwd_flag": pl.Utf8,
            "payment_type": pl.Int8,
            "fare_amount": pl.Float64,
            "extra": pl.Float64,
            "mta_tax": pl.Float64,
            "improvement_surcharge": pl.Float64,
            "tip_amount": pl.Float64,
            "tolls_amount": pl.Float64,
            "total_amount": pl.Float64,
            "congestion_surcharge": pl.Float64,
            "ehail_fee": pl.Float64,
            "trip_type": pl.Int8,
        },
    ).rename({
        "VendorID": "vendor_id",
        "lpep_pickup_datetime": "lpep_pickup_datetime",
        "lpep_dropoff_datetime": "lpep_dropoff_datetime",
        "passenger_count": "passenger_count",
        "trip_distance": "trip_distance",
        "PULocationID": "pu_location_id",
        "DOLocationID": "do_location_id",
        "RatecodeID": "ratecode_id",
        "store_and_fwd_flag": "store_and_fwd_flag",
        "payment_type": "payment_type",
        "fare_amount": "fare_amount",
        "extra": "extra",
        "mta_tax": "mta_tax",
        "improvement_surcharge": "improvement_surcharge",
        "tip_amount": "tip_amount",
        "tolls_amount": "tolls_amount",
        "total_amount": "total_amount",
        "congestion_surcharge": "congestion_surcharge",
        "ehail_fee": "ehail_fee",
        "trip_type": "trip_type",
    })
    df.write_database(
        table_name=table_name,
        connection=conn_string,
        engine="adbc",
        if_table_exists="append",
    )
    logger.info("Serialization complete")


with DAG(
    dag_id="op_taxi_green_csv_to_postgres.py",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2020, 12, 1),
    schedule="@monthly",
    catchup=True,
    concurrency=2,
    tags=["operator", "polars", "pandas", "postgres"],
):
    dataset_url: str = "{base_url}/download/{dataset}/{filename}".format(
        base_url="https://github.com/DataTalksClub/nyc-tlc-data/releases",
        dataset="green",
        filename="green_tripdata_{{ execution_date.strftime('%Y-%m') }}.csv.gz",
    )
    xcom_id: str = Path(dataset_url).name

    fetch_dataset = PythonOperator(
        task_id="fetch_green_taxi_dataset",
        python_callable=fetch_dataset,
        op_kwargs=dict(url=dataset_url, xcom_id=xcom_id),
    )

    persist_to_postgres = PythonOperator(
        task_id="postgres_serialization",
        python_callable=persist_with,
        op_kwargs=dict(
            conn_string="postgres://postgres:postgres@ingest-db:5432/nyc_taxi",
            table_name="green_taxi_trips",
            xcom_id=xcom_id,
        ),
    )

    fetch_dataset >> persist_to_postgres

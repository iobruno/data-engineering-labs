from os import getenv
from pathlib import Path

from box import Box
from loguru import logger
from sqlalchemy import create_engine, exc, text
from typer import BadParameter, Context, Option, Typer

from app.df_fetcher import PandasFetcher, PolarsFetcher
from app.processor import (
    FhvProcessor,
    GreenTaxiProcessor,
    YellowTaxiProcessor,
    ZoneLookupProcessor,
    progress,
)

cli = Typer(no_args_is_help=True)


def load_conf() -> Box:
    config_path = Path(__file__).parent.parent / "datasets.yaml"
    return Box.from_yaml(filename=config_path)


def test_db_conn(conn_str: str):
    engine = create_engine(conn_str)
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
            logger.info("Connection successfully established!")
    except exc.OperationalError as err:
        raise BadParameter(f"Missing db credentials in ENV variables - {err}") from err


@cli.callback()
def callback(ctx: Context):
    db_user = getenv("DB_USERNAME")
    db_pass = getenv("DB_PASSWORD")
    db_name = getenv("DB_NAME", "nyc_taxi")
    db_host = getenv("DB_HOST", "localhost")
    db_port = getenv("DB_PORT", 5432)

    adbc_conn_str = f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    conn_str = f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    logger.info("Attempting to connect to Postgresql with env vars...")

    test_db_conn(conn_str)
    ctx.obj = {"conn_string": conn_str, "adbc_conn_string": adbc_conn_str}


@cli.command(name="ingest", help="CLI app to extract NYC Trips data and load into Postgres")
def ingest_db(
    ctx: Context,
    yellow: bool = Option(False, "--yellow", "-y", help="Fetch Yellow taxi dataset"),
    green: bool = Option(False, "--green", "-g", help="Fetch Green cab dataset"),
    fhv: bool = Option(False, "--fhv", "-f", help="Fetch FHV cab dataset"),
    zones: bool = Option(False, "--zones", "-z", help="Fetch Zone lookup dataset"),
    use_polars: bool = Option(False, "--use-polars", help="Feature flag to use Polars"),
):
    if not any([yellow, green, fhv, zones]):
        raise BadParameter("You must either specify at least one dataset flag (-z | -y | -g | -f)")

    if use_polars:
        conn_str = ctx.obj.get("adbc_conn_string")
        fetcher = PolarsFetcher()
    else:
        conn_str = ctx.obj.get("conn_string")
        fetcher = PandasFetcher()

    logger.info("Loading datasets...")
    datasets = load_conf()

    with progress:
        if green:
            endpoints = datasets.green_taxi_trip_data
            processor = GreenTaxiProcessor(fetcher, conn_str)
            processor.run(endpoints)

        if yellow:
            endpoints = datasets.yellow_taxi_trip_data
            processor = YellowTaxiProcessor(fetcher, conn_str)
            processor.run(endpoints)

        if fhv:
            endpoints = datasets.fhv_trip_data
            processor = FhvProcessor(fetcher, conn_str)
            processor.run(endpoints)

        if zones:
            endpoints = datasets.zone_lookups
            processor = ZoneLookupProcessor(fetcher, conn_str)
            processor.run(endpoints)

    logger.info("All done!")

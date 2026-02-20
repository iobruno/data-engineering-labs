from os import getenv

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType


def join_dfs_with_spark_sql(spark: SparkSession) -> DataFrame:
    return spark.sql(
        """
        WITH t_fhv AS (
            SELECT
                dispatching_base_num,
                Affiliated_base_number as affiliated_base_num,
                pickup_datetime,
                dropOff_datetime as dropoff_datetime,
                PUlocationID as pickup_location_id,
                DOlocationID as dropoff_location_id
            FROM fhv
        ),

        t_zones AS (
            SELECT
                LocationID as location_id,
                Borough as borough,
                Zone as zone,
                service_zone
            FROM zones
        )

        SELECT
            f.dispatching_base_num,
            f.affiliated_base_num,
            -- Pickup Location
            f.pickup_datetime,
            pu.zone as pickup_zone,
            pu.service_zone as pickup_service_zone,
            -- Dropoff Location
            f.dropoff_location_id,
            do.zone as dropoff_zone,
            do.service_zone as dropoff_service_zone
        FROM
            t_fhv f
        INNER JOIN t_zones pu ON f.pickup_location_id  = pu.location_id
        INNER JOIN t_zones do ON f.dropoff_location_id = do.location_id
    """
    )


def get_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.driver.memory", "2g")
        .config("spark.executor.memory", "4g")
        .config("spark.cores.max", 8)
        .appName("pyspark-4.0-pipeline")
        .getOrCreate()
    )

def main():
    spark = get_spark_session()
    logger = spark._jvm.org.apache.log4j.LogManager.getLogger(__name__)

    fhv_gcs_path = getenv(
        key="FHV_GCS_PATH",
        default="gs://iobruno-lakehouse-raw/nyc_tlc_dataset/fhv_trip_data/fhv_tripdata_2019-01.snappy.parquet",
    )
    zone_lookup_gcs_path = getenv(
        key="ZONE_LOOKUP_PATH",
        default="gs://iobruno-lakehouse-raw/nyc_tlc_dataset/zone_lookup/taxi_zone_lookup.csv.gz",
    )

    logger.info(f"Now fetching 'FHV' Dataset: {fhv_gcs_path}")
    fhv: DataFrame = spark.read.parquet(fhv_gcs_path)
    fhv.createTempView("fhv")

    logger.info(f"Now fetching 'Zone Lookup' Dataset: {zone_lookup_gcs_path}")
    zones: DataFrame = (
        spark.read
        .option("header", True)
        .schema(
            StructType([
                StructField("LocationID", IntegerType(), True),
                StructField("Borough", StringType(), True),
                StructField("Zone", StringType(), True),
                StructField("service_zone", StringType(), True),
            ])
        )
        .csv(path=zone_lookup_gcs_path)
    )
    zones.createTempView("zones")

    # Join DataFrames with SparkSQL
    logger.info("Joining DataFrames with SparkSQL")
    sdf = join_dfs_with_spark_sql(spark)

    logger.info("Preparing to write resulting DataFrame...")
    (
        sdf.write
        .option("compression", "snappy")
        .mode("overwrite")
        .parquet("gs://iobruno-lakehouse-raw/spark-warehouse/")
    )

    logger.info("All done!")
    spark.stop()


if __name__ == "__main__":
    main()

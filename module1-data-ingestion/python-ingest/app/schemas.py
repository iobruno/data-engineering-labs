from dataclasses import dataclass, replace
from typing import Self

import polars as pl


@dataclass
class Field:
    name: str
    polarsType: type[pl.DataType]
    arrowDataType: str
    alias: str | None = None

    @property
    def col(self) -> str:
        return self.alias or self.name

    def as_(self, value: str) -> Self:
        return replace(self, alias=value)


class Schema:
    fields: list[Field]

    @classmethod
    def cols(cls) -> list[str]:
        return [field.col for field in cls.fields]

    @classmethod
    def to_polars(cls) -> dict:
        return {field.col: field.polarsType for field in cls.fields}

    @classmethod
    def to_arrow(cls) -> dict:
        return {field.col: field.arrowDataType for field in cls.fields}


class GreenTaxiSchema(Schema):
    fields = [
        Field("VendorID", pl.Int32, "Int64").as_("vendor_id"),
        Field("lpep_pickup_datetime", pl.Datetime, "datetime64[s]"),
        Field("lpep_dropoff_datetime", pl.Datetime, "datetime64[s]"),
        Field("store_and_fwd_flag", pl.String, "string"),
        Field("RatecodeID", pl.Int8, "Int64").as_("ratecode_id"),
        Field("PULocationID", pl.Int32, "Int64").as_("pu_location_id"),
        Field("DOLocationID", pl.Int32, "Int64").as_("do_location_id"),
        Field("passenger_count", pl.Int8, "Int64"),
        Field("trip_distance", pl.Float64, "float64"),
        Field("fare_amount", pl.Float64, "float64"),
        Field("extra", pl.Float64, "float64"),
        Field("mta_tax", pl.Float64, "float64"),
        Field("tip_amount", pl.Float64, "float64"),
        Field("tolls_amount", pl.Float64, "float64"),
        Field("ehail_fee", pl.Float64, "float64"),
        Field("improvement_surcharge", pl.Float64, "float64"),
        Field("total_amount", pl.Float64, "float64"),
        Field("payment_type", pl.Int8, "Int64"),
        Field("trip_type", pl.Int8, "Int64"),
        Field("congestion_surcharge", pl.Float64, "float64"),
    ]


class YellowTaxiSchema(Schema):
    fields = [
        Field("VendorID", pl.Int32, "Int64").as_("vendor_id"),
        Field("tpep_pickup_datetime", pl.Datetime, "datetime64[s]"),
        Field("tpep_dropoff_datetime", pl.Datetime, "datetime64[s]"),
        Field("passenger_count", pl.Int8, "Int64"),
        Field("trip_distance", pl.Float64, "float64"),
        Field("RatecodeID", pl.Int8, "Int64").as_("ratecode_id"),
        Field("store_and_fwd_flag", pl.String, "string"),
        Field("PULocationID", pl.Int32, "Int64").as_("pu_location_id"),
        Field("DOLocationID", pl.Int32, "Int64").as_("do_location_id"),
        Field("payment_type", pl.Int8, "Int64"),
        Field("fare_amount", pl.Float64, "float64"),
        Field("extra", pl.Float64, "float64"),
        Field("mta_tax", pl.Float64, "float64"),
        Field("tip_amount", pl.Float64, "float64"),
        Field("tolls_amount", pl.Float64, "float64"),
        Field("improvement_surcharge", pl.Float64, "float64"),
        Field("total_amount", pl.Float64, "float64"),
        Field("congestion_surcharge", pl.Float64, "float64"),
    ]


class FhvSchema(Schema):
    fields = [
        Field("dispatching_base_num", pl.String, "string"),
        Field("pickup_datetime", pl.String, "datetime64[s]"),
        Field("dropOff_datetime", pl.String, "datetime64[s]").as_("dropoff_datetime"),
        Field("PUlocationID", pl.Int32, "Int64").as_("pu_location_id"),
        Field("DOlocationID", pl.Int32, "Int64").as_("do_location_id"),
        Field("SR_Flag", pl.String, "string").as_("sr_flag"),
        Field("Affiliated_base_number", pl.String, "string").as_("affiliated_base_number"),
    ]


class ZoneLookupSchema(Schema):
    fields = [
        Field("LocationID", pl.Int32, "Int64").as_("location_id"),
        Field("Borough", pl.String, "string").as_("borough"),
        Field("Zone", pl.String, "string").as_("zone"),
        Field("service_zone", pl.String, "string"),
    ]

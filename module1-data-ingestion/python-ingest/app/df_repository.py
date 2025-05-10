from abc import ABCMeta, abstractmethod
from typing import Literal

import pandas as pd
import polars as pl

type Engine = Literal["adbc", "sqlalchemy"]
type WriteDisposition = Literal["replace", "append"]


class SQLRepo(metaclass=ABCMeta):
    def __init__(self, conn_string: str):
        self.conn_string = conn_string

    def save(self, df: pd.DataFrame | pl.DataFrame, write_disposition: WriteDisposition):
        if isinstance(df, pl.DataFrame):
            return self.save_polars_df(df, write_disposition, "adbc")
        elif isinstance(df, pd.DataFrame):
            return self.save_pandas_df(df, write_disposition)
        raise RuntimeError("Unsupported DataFrame type. Only pandas or polars are supported")

    def save_polars_df(self, df: pl.DataFrame, write_disposition: WriteDisposition, engine: Engine):
        return df.write_database(
            table_name=self.tbl_name,
            connection=self.conn_string,
            engine=engine,
            if_table_exists=write_disposition,
        )

    def save_pandas_df(self, df: pd.DataFrame, write_disposition):
        return df.to_sql(
            name=self.tbl_name,
            con=self.conn_string,
            if_exists=write_disposition,
            index=False,
        )

    def save_all(self, chunks: list[pd.DataFrame]):
        for chunk in chunks:
            yield self.save(df=chunk, write_disposition="append")

    @property
    @abstractmethod
    def tbl_name(self) -> str:
        raise NotImplementedError()


class GreenTaxiRepo(SQLRepo):
    @property
    def tbl_name(self) -> str:
        return "green_taxi_trips"


class YellowTaxiRepo(SQLRepo):
    @property
    def tbl_name(self) -> str:
        return "yellow_taxi_trips"


class FhvRepo(SQLRepo):
    @property
    def tbl_name(self) -> str:
        return "fhv_trips"


class ZoneLookupRepo(SQLRepo):
    @property
    def tbl_name(self) -> str:
        return "zone_lookup"

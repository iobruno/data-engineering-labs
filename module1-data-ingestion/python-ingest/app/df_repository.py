from abc import ABCMeta, abstractmethod
from typing import Literal

import pandas as pd
import polars as pl

type Engine = Literal["adbc", "sqlalchemy"]
type WriteDisposition = Literal["replace", "append"]


class DataFrameRepo(metaclass=ABCMeta):

    def __init__(self, tbl_name: str, conn_str: str):
        self.tbl_name = tbl_name
        self.conn_str = conn_str

    @abstractmethod
    def save(self, df, write_disposition):
        raise NotImplementedError

    def save_all(self, chunks: list[pd.DataFrame] | list[pl.DataFrame]):
        for chunk in chunks:
            yield self.save(df=chunk, write_disposition="append")


class PandasDataFrameRepo(DataFrameRepo):

    def save(self, df, write_disposition):
        return df.to_sql(
            name=self.tbl_name,
            con=self.conn_str,
            if_exists=write_disposition,
            index=False,
        )


class PolarsDataFrameRepo(DataFrameRepo):

    def save(self, df, write_disposition: WriteDisposition, engine: Engine = "adbc"):
        return df.write_database(
            table_name=self.tbl_name,
            connection=self.conn_str,
            engine=engine,
            if_table_exists=write_disposition,
        )

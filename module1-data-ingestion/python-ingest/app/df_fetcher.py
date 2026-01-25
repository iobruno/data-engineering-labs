from abc import ABCMeta, abstractmethod

import pandas as pd
import polars as pl


class DataframeFetcher(metaclass=ABCMeta):
    def with_schema(self, schema: dict):
        def fetch_csv(endpoint: str) -> pl.DataFrame:
            return self.fetch_csv(endpoint, schema)

        return fetch_csv

    @abstractmethod
    def fetch_csv(self, endpoint: str, schema: dict = None) -> pl.DataFrame | pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def fetch_parquet(self, endpoint: str) -> pl.DataFrame | pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def slice_in_chunks(self, df, chunk_size: int = 100_000) -> list[pl.DataFrame | pd.DataFrame]:
        raise NotImplementedError()


class PolarsFetcher(DataframeFetcher):
    def fetch_csv(self, endpoint: str, schema: dict = None) -> pl.DataFrame:
        return pl.read_csv(endpoint, schema_overrides=schema)

    def fetch_parquet(self, endpoint: str) -> pl.DataFrame:
        return pl.read_parquet(endpoint)

    def slice_in_chunks(self, df, chunk_size: int = 100_000) -> list[pl.DataFrame]:
        return [
            df.slice(offset=chunk_id, length=chunk_size)
            for chunk_id in range(0, len(df), chunk_size)
        ]


class PandasFetcher(DataframeFetcher):
    def fetch_csv(self, endpoint: str, schema: dict = None) -> pd.DataFrame:
        return pd.read_csv(endpoint, engine="pyarrow", dtype=schema)

    def fetch_parquet(self, endpoint: str) -> pd.DataFrame:
        return pd.read_parquet(endpoint)

    def slice_in_chunks(self, df, chunk_size: int = 100_000) -> list[pd.DataFrame]:
        return [
            df.iloc[chunk_id : chunk_id + chunk_size] for chunk_id in range(0, len(df), chunk_size)
        ]

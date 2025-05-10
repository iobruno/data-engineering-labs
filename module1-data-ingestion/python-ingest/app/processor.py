from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Literal, Type

from rich.progress import BarColumn, Progress, TaskID, TextColumn, TimeElapsedColumn

from app.df_fetcher import DataframeFetcher, PandasFetcher, PolarsFetcher
from app.df_repository import FhvRepo, GreenTaxiRepo, SQLRepo, YellowTaxiRepo, ZoneLookupRepo
from app.schemas import FhvSchema, GreenTaxiSchema, Schema, YellowTaxiSchema, ZoneLookupSchema

progress = Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "Chunk: {task.completed}/{task.total} •",
    "[progress.percentage]{task.percentage:>3.1f}% •",
    TimeElapsedColumn(),
)


class Processor(metaclass=ABCMeta):
    def __init__(self, fetcher: DataframeFetcher, conn_str: str):
        self.repo = self.repo(conn_str)
        self.fetcher = fetcher

    def extract_and_load_with(
        self,
        endpoints: list[str],
        write_disposition: Literal["replace", "append"],
        tasks: list[TaskID],
    ):
        if not endpoints:
            return

        tid, *remain_tasks = tasks
        endpoint, *remain_endpoints = endpoints

        df = self.fetcher.fetch_csv(endpoint, schema=self._fetch_schema())
        slices = self.fetcher.slice_in_chunks(df)
        chunk, *remain_chunks = slices
        completeness, total_parts = 1, len(slices)

        progress.update(task_id=tid, completed=0, total=total_parts)
        progress.start_task(task_id=tid)

        # Required since polars.df doesn't create the table in 'append' mode if it doesn't exist
        self.repo.save(chunk, write_disposition)
        progress.update(task_id=tid, completed=completeness, total=total_parts)

        for _ in self.repo.save_all(remain_chunks):
            completeness += 1
            progress.update(task_id=tid, completed=completeness, total=total_parts)

        self.extract_and_load_with(remain_endpoints, "append", remain_tasks)

    def run(self, endpoints: list[str]):
        tasks = self.gen_progress_tasks_for(endpoints)
        self.extract_and_load_with(endpoints, "replace", tasks)

    @classmethod
    def gen_progress_tasks_for(cls, endpoints: list[str]) -> list[TaskID]:
        filenames = [Path(endpoint).stem for endpoint in endpoints]
        return [
            progress.add_task(name, start=False, total=float("inf"), completed=0)
            for name in filenames
        ]

    def _fetch_schema(self) -> dict:
        if isinstance(self.fetcher, PolarsFetcher):
            return self.schema().polars()
        elif isinstance(self.fetcher, PandasFetcher):
            return self.schema().pyarrow()
        raise NotImplementedError()

    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError()

    @abstractmethod
    def repo(self, conn_str: str) -> SQLRepo:
        raise NotImplementedError()


class GreenTaxiProcessor(Processor):
    def schema(self) -> Type[GreenTaxiSchema]:
        return GreenTaxiSchema

    def repo(self, conn_str: str) -> SQLRepo:
        return GreenTaxiRepo(conn_str)


class YellowTaxiProcessor(Processor):
    def schema(self) -> Type[Schema]:
        return YellowTaxiSchema

    def repo(self, conn_str: str) -> SQLRepo:
        return YellowTaxiRepo(conn_str)


class FhvProcessor(Processor):
    def schema(self) -> Type[Schema]:
        return FhvSchema

    def repo(self, conn_str) -> SQLRepo:
        return FhvRepo(conn_str)


class ZoneLookupProcessor(Processor):
    def schema(self) -> Type[Schema]:
        return ZoneLookupSchema

    def repo(self, conn_str) -> SQLRepo:
        return ZoneLookupRepo(conn_str)

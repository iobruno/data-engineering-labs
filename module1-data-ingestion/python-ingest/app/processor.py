from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import ClassVar, Literal

from rich.progress import BarColumn, Progress, TaskID, TextColumn, TimeElapsedColumn

from app.df_fetcher import DataframeFetcher, PolarsFetcher
from app.df_repository import DataFrameRepo
from app.schemas import FhvSchema, GreenTaxiSchema, Schema, YellowTaxiSchema, ZoneLookupSchema

progress = Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "Chunk: {task.completed}/{task.total} •",
    "[progress.percentage]{task.percentage:>3.1f}% •",
    TimeElapsedColumn(),
)


class Processor(metaclass=ABCMeta):

    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError

    @abstractmethod
    def fetcher(self) -> DataframeFetcher:
        raise NotImplementedError

    @abstractmethod
    def repo(self) -> DataFrameRepo:
        raise NotImplementedError

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

        df = self.fetcher.fetch_csv(endpoint, schema=self.schema)
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


class GreenTaxiProcessor(Processor):

    def fetcher(self) -> DataframeFetcher:
        return PolarsFetcher()

    def schema(self):
        return GreenTaxiSchema.to_polars()

    def repo(self):
        return GreenTaxiRepo()




class YellowTaxiProcessor(Processor):
    schema = YellowTaxiSchema
    repo_cls = YellowTaxiRepo


class FhvProcessor(Processor):
    schema = FhvSchema
    repo_cls = FhvRepo


class ZoneLookupProcessor(Processor):
    schema = ZoneLookupSchema
    repo_cls = ZoneLookupRepo

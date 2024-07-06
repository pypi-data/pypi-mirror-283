"""Track delegated processes with rich progress meters.

Based on: https://www.deanmontgomery.com/2022/03/24/rich-progress-and-multiprocessing

"""

import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from multiprocessing.managers import DictProxy
from time import sleep

from beartype.typing import Any, Callable, List, TypeVar, Union
from rich.progress import BarColumn, Progress, ProgressColumn, TaskID, TimeElapsedColumn, TimeRemainingColumn

_ItemT = TypeVar('_ItemT', bound=Any)
"""Iterated item in the data."""


_DelegatedTask = Callable[
    [
        TaskID,
        DictProxy,  # type: ignore[type-arg]
        list[_ItemT],
    ],
    Any,
]


def _chunked(data: List[_ItemT], count: int) -> List[List[_ItemT]]:
    """Chunk the list of data into equally sized lists."""
    # TODO: See below link for other options for chunking
    #   https://realpython.com/how-to-split-a-python-list-into-chunks/
    size = len(data)
    chunk_size, chunk_rem = size // count, size % count
    chunk_size += int(math.ceil(chunk_rem / size))
    return [data[ix : ix + chunk_size] for ix in range(0, size, chunk_size)]


def pretty_process(
    delegated_task: _DelegatedTask,  # type: ignore[type-arg]
    *,
    data: List[_ItemT],
    num_workers: int = 3,
    num_cpus: int = 4,
) -> Any:
    """Run a task in parallel to process all provided data.

    Uses `rich` to display pretty progress bars

    Args:
    ----
        delegated_task: must call `shared_progress[task_id] += 1` on each item in data
        data: the list of data to distribute
        num_workers: number of worker processes
        num_cpus: number of CPUs

    """
    # Docs: https://rich.readthedocs.io/en/latest/progress.html
    columns: List[Union[str, ProgressColumn]] = [
        '[progress.description]{task.description}',
        BarColumn(),
        '[progress.percentage]{task.percentage:>3.0f}%',
        TimeRemainingColumn(),
        TimeElapsedColumn(),
    ]
    with Progress(*columns, refresh_per_second=1) as progress:  # noqa: SIM117 (Py>3.9)
        # Share state between process and workers
        with multiprocessing.Manager() as manager:
            shared_progress = manager.dict()
            jobs = []
            totals = {}
            task_id_all = progress.add_task('[green]All jobs progress:')

            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                for ix, chunk in enumerate(_chunked(data, count=num_cpus)):
                    task_id = progress.add_task(f'task {ix}')
                    shared_progress[task_id] = 0
                    totals[task_id] = len(chunk)
                    jobs.append(executor.submit(delegated_task, task_id, shared_progress, chunk))

                # Update progress bar from shared state
                remaining = len(jobs)
                while remaining:
                    n_done = 0
                    for task_id, latest in shared_progress.items():
                        n_done += latest
                        progress.update(task_id, completed=latest, total=totals[task_id])
                    progress.update(task_id_all, completed=n_done, total=len(data))
                    remaining = len(jobs) - sum(job.done() for job in jobs)

                # Collect results and catch and errors
                return [job.result() for job in jobs]


# Note: this function can't be in the if-block below
def __long_task(task_id: int, shared_progress: DictProxy, data: List[_ItemT]) -> Any:  # type: ignore[type-arg]
    """Run a long example task."""
    for _val in data:
        sleep(1)
        shared_progress[task_id] += 1
    return True


if __name__ == '__main__':

    def _demo() -> None:
        """Run demo with: 'poetry run python -m shoal.pretty_process'."""
        # Resolve number of cores or specified maximum
        num_cpus = 4
        try:
            import psutil  # pyright: ignore[reportMissingModuleSource] # noqa: PLC0415

            num_cpus = psutil.cpu_count(logical=False)
        except Exception as exc:
            print(exc)  # noqa: T201

        result = pretty_process(__long_task, data=[*range(23)], num_workers=num_cpus)
        print(result)  # noqa: T201

    _demo()

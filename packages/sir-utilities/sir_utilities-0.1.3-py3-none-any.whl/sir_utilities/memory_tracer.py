from abc import ABC
from datetime import datetime, timedelta
from logging import Logger
import threading
import time
import tracemalloc
from typing import Any, List

# import gc
# from pympler.asizeof import asizeof  # type: ignore

from sir_utilities.date_time import now_utc_iso
from sir_utilities.logger import module_logger
from sir_utilities.unit_conversion import convert_bytes


class MemoryTracerLogger(ABC):
    def log_memory_allocations(
        self,
        logger: Logger,
        top_n: int,
        top_statistics: List[tracemalloc.StatisticDiff] | list[tracemalloc.Statistic],
    ) -> None:
        sorted_stats = sorted(
            top_statistics[:top_n],
            key=lambda stat: stat.size,
            reverse=True,
        )
        message = [f"Top {top_n} memory allocations by size:"]
        message.extend(str(stat) for stat in sorted_stats[:top_n])
        logger.info("\n".join(message))

    def log_object_memory_usage(
        self,
        logger: Logger,
        top_n: int,
        top_objects: List[tuple[Any, int]],
    ) -> None:
        message = [f"Top {top_n} objects in memory by size:"]
        for obj, size in top_objects:
            message.extend(f"{type(obj)}: {convert_bytes(size)}")
        logger.info("\n".join(message))


class MemoryTracer(MemoryTracerLogger):
    def __init__(self) -> None:
        self._name = type(self).__name__
        self._logger = module_logger(self._name)
        self._cached_snapshot: tracemalloc.Snapshot | None = None
        self._last_trace: datetime | None = None

    def start(self, top_n: int = 20, interval_seconds: int = 180) -> None:
        tracemalloc.start()

        t = threading.Thread(
            name=self._name,
            target=self.perform_memory_tracking,
            args=[top_n, interval_seconds],
        )
        t.start()

    def stop(self) -> None:
        tracemalloc.stop()

    def perform_memory_tracking(self, top_n: int, interval_seconds: int) -> None:
        while tracemalloc.is_tracing():
            if self._trace_is_due(interval_seconds):
                self._take_memory_snapshot(top_n)
                # self._dispatch_get_top_n_objects(top_n)
                self._last_trace = now_utc_iso()
            time.sleep(min(15, interval_seconds))

    def _trace_is_due(self, interval_seconds: int) -> bool:
        if self._last_trace is None:
            return True

        return now_utc_iso() - self._last_trace > timedelta(seconds=interval_seconds)

    def _take_memory_snapshot(self, top_n: int) -> None:
        snapshot = tracemalloc.take_snapshot()
        top_stats = None
        if self._cached_snapshot:
            top_stats = snapshot.compare_to(
                self._cached_snapshot,
                "lineno",
            )
        else:
            top_stats = snapshot.statistics("lineno")

        if top_stats:
            self.log_memory_allocations(self._logger, top_n, top_stats)

        self._cached_snapshot = snapshot

    # def _dispatch_get_top_n_objects(self, top_n: int) -> None:
    #     name = "object_size_tracking"
    #     if not find_thread_by_name(name):
    #         t = threading.Thread(
    #             target=self._get_top_n_objects,
    #             args=[top_n],
    #             name=name,
    #         )
    #         t.start()

    # def _get_top_n_objects(self, top_n: int) -> None:
    #     gc.collect()  # Clean up first
    #     objects = gc.get_objects()
    #     try:
    #         sizes: List[Tuple[Any, int]] = []
    #         for obj in objects:
    #             try:
    #                 size = asizeof(obj)
    #                 if len(sizes) < top_n:
    #                     sizes.append((obj, size))
    #                     sizes.sort(key=lambda x: x[1], reverse=True)
    #                 elif size > sizes[-1][1]:
    #                     # If the size is larger than the smallest size in the list, replace the smallest object
    #                     sizes[-1] = (obj, size)
    #                     sizes.sort(key=lambda x: x[1], reverse=True)
    #             except Exception:
    #                 continue
    #         top_objects = sorted(sizes, key=lambda x: x[1], reverse=True)[:top_n]
    #         self.log_object_memory_usage(self._logger, top_n, top_objects)
    #     except Exception:
    #         pass


# Test run
# from sir_utilities.logger import LogMode, module_logger, setup_logging

# print(sys.path)
# setup_logging(LogMode.DEBUG_PRINT_ONLY)
# mt = MemoryTracer()
# mt.start(interval_seconds=30)
# time.sleep(600)
# mt.stop()

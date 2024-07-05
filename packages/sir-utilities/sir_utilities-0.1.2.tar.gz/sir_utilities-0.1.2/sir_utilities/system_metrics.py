from abc import ABC
from datetime import datetime, timedelta
from logging import Logger
import threading
import time

import psutil

from sir_utilities.date_time import now_utc_iso
from sir_utilities.logger import module_logger


class SystemMetricsLogger(ABC):
    def log_cpu_usage(self, logger: Logger, cpu_usage: str) -> None:
        msg = f"CPU usage: {cpu_usage}%."
        logger.info(msg)

    def log_memory_usage(
        self,
        logger: Logger,
        memory_total: float,
        memory_used: float,
        used_pct: float,
    ) -> None:
        mem_used_mb = f"{memory_used / (1024 ** 2):.2f}MB"
        mem_total_mb = f"{memory_total / (1024 ** 2):.2f}MB"
        percentage = f"{used_pct:.2f}%"
        usage_str = f"{mem_used_mb} / {mem_total_mb} ({percentage})"
        msg = f"RAM usage: {usage_str}."
        logger.info(msg)

    def log_swap_usage(
        self,
        logger: Logger,
        swap_total: float,
        swap_used: float,
        used_pct: float,
    ) -> None:
        swap_used_mb = f"{swap_used / (1024 ** 2):.2f}MB"
        swap_total_mb = f"{swap_total / (1024 ** 2):.2f}MB"
        percentage = f"{used_pct:.2f}%"
        usage_str = f"{swap_used_mb} / {swap_total_mb} ({percentage})"
        msg = f"Swap usage: {usage_str}."
        logger.info(msg)


class SystemMetrics(SystemMetricsLogger):
    def __init__(self) -> None:
        self._name = type(self).__name__
        self._logger = module_logger(type(self).__name__)
        self._running = False
        self._last_metrics: datetime | None = None

    def start(self, interval_seconds: int = 10) -> None:
        self._running = True
        t = threading.Thread(
            name=self._name,
            target=self.monitor_system_metrics,
            args=[interval_seconds],
        )
        t.start()

    def stop(self) -> None:
        self._running = False

    def monitor_system_metrics(self, interval_seconds: int):
        while self._running:
            if self._metrics_are_due(interval_seconds):
                self._cpu_usage()
                self._memory_usage()
                self._swap_usage()
                self._last_metrics = now_utc_iso()
            time.sleep(min(15, interval_seconds))

    def _metrics_are_due(self, interval_seconds: int) -> bool:
        if self._last_metrics is None:
            return True

        return now_utc_iso() - self._last_metrics > timedelta(seconds=interval_seconds)

    def _cpu_usage(self) -> None:
        cpu_usage_pct = str(psutil.cpu_percent())
        self.log_cpu_usage(self._logger, cpu_usage_pct)

    def _memory_usage(self) -> None:
        # Memory usage
        memory = psutil.virtual_memory()

        # Metrics
        memory_total = memory.total
        memory_used = memory.used
        used_pct = (memory_used / memory_total) * 100

        self.log_memory_usage(self._logger, memory_total, memory_used, used_pct)

    def _swap_usage(self) -> None:
        # Memory usage
        swap_memory = psutil.swap_memory()

        # Metrics
        swap_total = swap_memory.total
        swap_used = swap_memory.used
        used_pct = (swap_used / swap_total) * 100 if swap_total > 0 else float(0)

        self.log_swap_usage(self._logger, swap_total, swap_used, used_pct)

from datetime import datetime, timedelta
import threading
import time
from typing import Any, Callable, Dict


class Cli:
    def __init__(self, stop_sequence: str = "stop") -> None:
        self._stop_sequence = stop_sequence
        self._running = False

    def running(self) -> bool:
        return self._running

    def start_cli(
        self,
        duration_seconds: int,
        callbacks: Dict[Callable[..., None], Any | None],
    ) -> None:
        self._running = True
        self._callbacks = callbacks
        t_count_down = threading.Thread(
            target=self._count_down,
            args=[duration_seconds],
            name="cli_count_down",
        )
        t_cli = threading.Thread(target=self.listen_for_input, name="cli_input")
        t_count_down.start()
        t_cli.start()

    def stop_cli(self) -> None:
        if self._running:
            self._running = False
            for callback, args in self._callbacks.items():
                if args:
                    callback(args)
                else:
                    callback()

    def _count_down(self, duration: int | None) -> None:
        if duration:
            start_time = datetime.now()
            stop_time = start_time + timedelta(seconds=duration)

            while self._running and not datetime.now() >= stop_time:
                time.sleep(5)

            elapsed = datetime.now() - start_time
            elapsed = timedelta(days=elapsed.days, seconds=elapsed.seconds)

            print(f"Bot ran for {elapsed} hours.")
            self.stop_cli()

    def listen_for_input(self) -> None:
        while self._running:
            user_input = input(f"\nEnter '{self._stop_sequence}' to stop the bot: ")
            if user_input.lower() == f"{self._stop_sequence}":
                break
        self.stop_cli()

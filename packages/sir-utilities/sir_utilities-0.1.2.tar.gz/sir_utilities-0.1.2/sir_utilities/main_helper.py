import time
from sir_utilities.thread_helper import find_thread_by_name


def keep_main_alive_for_thread(thread_name: str) -> None:
    if thread := find_thread_by_name(f"{thread_name}"):
        while thread.is_alive():
            time.sleep(5)

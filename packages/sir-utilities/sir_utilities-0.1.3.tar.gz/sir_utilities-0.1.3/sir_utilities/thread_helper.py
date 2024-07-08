import threading


def find_thread_by_name(thread_name: str) -> threading.Thread | None:
    return next(
        (thread for thread in threading.enumerate() if thread.name == thread_name),
        None,
    )

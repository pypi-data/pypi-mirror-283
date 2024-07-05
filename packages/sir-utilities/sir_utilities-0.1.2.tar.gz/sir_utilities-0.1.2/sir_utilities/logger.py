from datetime import datetime
from enum import Enum, auto
import os
import logging
from sir_utilities.find_root import find_root


def create_log_files_dir(project_root_path: str = find_root()) -> str:
    log_files_dir = os.path.join(project_root_path, "log_files")

    # Check if the directory exists - if not create
    if not os.path.exists(log_files_dir):
        os.makedirs(log_files_dir)

    return log_files_dir


class LogMode(Enum):
    DEBUG = auto()
    INFO = auto()
    DEBUG_PRINT_ONLY = auto()
    INFO_PRINT_ONLY = auto()


def setup_logging(mode: LogMode, log_file_dir: str = create_log_files_dir()) -> None:
    default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    today = datetime.now().strftime("%Y-%m-%d")

    if mode == LogMode.DEBUG:
        log_path = os.path.join(log_file_dir, f"debug_log_{today}.log")
        logging.basicConfig(
            force=True,
            level=logging.DEBUG,
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
            format=default_format,
        )
    elif mode == LogMode.INFO:
        log_path = os.path.join(log_file_dir, f"live_log_{today}.log")
        logging.basicConfig(
            force=True,
            level=logging.INFO,
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
            format=default_format,
        )
    elif mode == LogMode.DEBUG_PRINT_ONLY:
        logging.basicConfig(
            force=True,
            level=logging.DEBUG,
            handlers=[logging.StreamHandler()],
            format=default_format,
        )
    elif mode == LogMode.INFO_PRINT_ONLY:
        logging.basicConfig(
            force=True,
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            format=default_format,
        )


def module_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.propagate = True
    return logger

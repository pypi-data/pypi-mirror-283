import os


def find_root(marker_file: str = "pyproject.toml") -> str:
    # Traverse project structure upwards until pyproject.toml is found
    temp_dir = start_dir = os.path.dirname(os.path.abspath(__file__))
    while temp_dir != "/":
        if _contains_marker_file(temp_dir, marker_file):
            return temp_dir
        temp_dir = os.path.dirname(temp_dir)
    raise FileNotFoundError(
        f"Project root not found (start: '{start_dir}', marker: '{marker_file}')."
    )


def _contains_marker_file(directory_path: str, marker_file: str) -> bool:
    pyproject_path = os.path.join(directory_path, marker_file)
    return os.path.exists(pyproject_path)

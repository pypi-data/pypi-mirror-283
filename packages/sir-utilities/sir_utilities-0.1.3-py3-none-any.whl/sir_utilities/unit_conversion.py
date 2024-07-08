from typing import List, Union


def convert_bytes(size_bytes: Union[int, float]) -> str:
    units: List[str] = ["B", "KiB", "MiB", "GiB", "TiB"]
    unit_index: int = 0

    # Iterate through units until the size is small enough
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1

    # Format size with unit
    return f"{size_bytes:.2f} {units[unit_index]}"

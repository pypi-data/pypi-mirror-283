from datetime import datetime, timezone
from dateutil import parser
from enum import Enum


class DateFormat(Enum):
    YMDHMSF_ISO = "%Y-%m-%dT%H:%M:%S.%fZ"
    YMDHMSF_ISO_OFFSET = "%Y-%m-%d %H:%M:%S%z"
    YMDHM = "%Y-%m-%d %H:%M"


def now_utc_iso() -> datetime:
    return datetime.now(timezone.utc)


def string_to_datetime(
    date_str: str,
) -> datetime:
    dt = parser.isoparse(date_str)
    return dt.astimezone(tz=timezone.utc)


def datetime_to_string(
    date: datetime,
    format: str = DateFormat.YMDHMSF_ISO_OFFSET.value,
) -> str:
    return date.strftime(format)

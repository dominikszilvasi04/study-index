from datetime import datetime
from study_index.formatters import format_file_size, format_timestamp


def test_format_file_size() -> None:
    assert format_file_size(0) == "0"
    assert format_file_size(1234567) == "1,234,567"


def test_format_timestamp() -> None:
    timestamp = datetime(2026, 9, 22, 14, 5).timestamp()
    assert format_timestamp(timestamp) == "2026-09-22 14:05"

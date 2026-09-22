from datetime import datetime


def format_file_size(size_bytes: int) -> str:
    return f"{size_bytes:,}"


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

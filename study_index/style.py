from pathlib import Path


def application_stylesheet() -> str:
    stylesheet_path = Path(__file__).with_name("application.qss")
    return stylesheet_path.read_text(encoding="utf-8")

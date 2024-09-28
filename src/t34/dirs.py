import os
from pathlib import Path


def get_templates_dir():
    path = os.path.dirname(os.path.abspath(__file__))
    path = Path(path)
    return path / "templates"


def get_translations_dir():
    path = os.path.dirname(os.path.abspath(__file__))
    path = Path(path)
    return path / "translations"

import os
from pathlib import Path

def current_user_dir() -> str:
    return os.getcwd()

def cli_dir(index) -> str:
    current_file = Path(__file__)
    return current_file.parents[index]



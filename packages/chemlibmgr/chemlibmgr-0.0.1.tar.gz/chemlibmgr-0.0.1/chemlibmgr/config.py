from pathlib import Path


def get_base_path():
    current_file_path = Path(__file__).resolve()
    base_path = current_file_path.parent
    return str(base_path)


CLMDIR = get_base_path()

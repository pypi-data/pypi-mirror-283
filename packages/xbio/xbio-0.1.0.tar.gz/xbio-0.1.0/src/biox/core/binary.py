from pathlib import Path
from typing import Dict, List
import os


class BinaryManager:
    search_path: List[Path] = []
    search_path = [Path(p) for p in os.environ.get("PATH", "").split(os.pathsep)]
    binary_path: Dict[str, Path] = {}

    @classmethod
    def __init__(cls, *args):
        for path in args:
            cls.add_search_path(path)

    @classmethod
    def add_search_path(cls, path: str):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Path {path} does not exist")
        cls.search_path.append(Path(path))

    @classmethod
    def search(cls, binary: str):
        if binary in cls.binary_path:
            return cls.binary_path[binary]
        for path in cls.search_path:
            path = Path(path)
            if (path / binary).exists():
                cls.binary_path[binary] = path / binary
                return cls.binary_path[binary]
        return None


def get_binary_path(binary: str):
    return BinaryManager.search(binary)

from typing import Dict, List
from pathlib import Path as _Path


__all__ = ["Path", "get_endswith_all", "get_paired_files", "DatasetManager"]


class Path:
    def __init__(self, path: str):
        self._path = _Path(path)

    def get_endswith_all(self, suffix: str):
        if not suffix.startswith("."):
            suffix = f".{suffix}"
        files = list(self._path.glob("*"))
        files = [file for file in files if file.suffix.lower() == suffix.lower()]
        return [file.name for file in files]

    def get_paired_files(self, suffix: str, strict: bool = True):
        if not suffix.startswith("."):
            suffix = f".{suffix}"
        files = list(self._path.glob("*"))
        files = [file for file in files if file.suffix.lower() == suffix.lower()]
        if strict:
            assert len(files) % 2 == 0, "Number of files should be even"
        else:
            files = files[: len(files) - (len(files) % 2)]
        files = sorted(files)
        return [(files[i].name, files[i + 1].name) for i in range(0, len(files), 2)]


def get_endswith_all(path: str, suffix: str):
    return Path(path).get_endswith_all(suffix)


def get_paired_files(path: str, suffix: str, strict: bool = True):
    return Path(path).get_paired_files(suffix, strict)

class DatasetManager:
    def __init__(self):
        self.__inputs: Dict[str, List[Dict[str, str]]] = {}
        self.__outputs: Dict[str, List[Dict[str, str]]] = {}

    

    def send_input(self, job_name: str, data: List[Dict[str, str]]):
        self.__inputs[job_name] = data

    def send_output(self, job_name: str, data: List[Dict[str, str]]):
        self.__outputs[job_name] = data

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def get_input(self, job_name: str):
        return self.__inputs.get(job_name, [])

    def get_output(self, job_name: str):
        return self.__outputs.get(job_name, [])

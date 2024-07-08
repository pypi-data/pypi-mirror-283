import os
from typing import Dict, Optional


class Configure:
    job_environment: Dict[str, Dict[str, str]] = {}
    job_input_dir: Dict[str, str] = {}
    job_output_dir: Dict[str, str] = {}
    pwd: str = ""

    def __init__(
        self,
        pwd: Optional[str],
        environment: Dict[str, Dict[str, str]],
        input_dir: Dict[str, str],
        output_dir: Dict[str, str],
    ):
        self.pwd = pwd or os.path.abspath(os.getcwd())
        self.job_environment = environment
        self.job_input_dir = input_dir
        self.job_output_dir = output_dir

    def add_job_environment(self, command: str, env_key: str, env_value: str):
        if command not in self.job_environment:
            self.job_environment[command] = {}
        self.job_environment[command][env_key] = env_value

    def add_job_input_dir(self, command: str, dir: str):
        self.job_input_dir[command] = dir

    def add_job_output_dir(self, command: str, dir: str):
        self.job_output_dir[command] = dir

    def get_job_environment(self, command: str) -> Dict[str, str]:
        return self.job_environment.get(command, {})

    def get_job_input_dir(self, command: str) -> str:
        return self.job_input_dir.get(command, self.pwd)

    def get_job_output_dir(self, command: str) -> str:
        return self.job_output_dir.get(command, self.pwd)


conf = Configure(pwd="", environment={}, input_dir={}, output_dir={})

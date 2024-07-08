from abc import ABC, abstractmethod
from typing import Dict
from biox.core.log import LoggingMixin
from biox.core.status import Status
from biox.core.command import Command
from biox.core.job import Job


class ExecuteABC(ABC, LoggingMixin):
    @abstractmethod
    def execute_command(self, command: Command, job: Job):
        pass

    @abstractmethod
    def set_environment(self, envs: Dict[str, str]): ...

    def execute_job(self, job: Job):
        self.set_environment(job.env)
        for command in job.commands:
            command.status = Status.RUNNING
            self.execute_command(command, job)
            command.status = Status.COMPLETED
        job.status = Status.COMPLETED


class ShellExecutor(ExecuteABC):
    def __init__(self):
        self._workflow = None

    def set_environment(self, envs: Dict[str, str]):
        pass

    def execute_command(self, command: Command, job: Job):
        self.log.info(f"Executing command {command.command_name}")
        self.log.info(f"Command: {command.command}")
        import time
        import random
        import subprocess

        time.sleep(random.randint(0, 1))
        p = subprocess.Popen(
            command.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = p.communicate()
        if p.returncode != 0:
            self.log.error(
                f"Command {command.command_name} failed with error code {p.returncode}"
            )
            self.log.error(f"Error: {err}")
            raise Exception(
                f"Command {command.command_name} failed with error code {p.returncode}"
            )
        else:
            self.log.info(f"Output: {out}")
        self.log.info(f"Command {command.command_name} executed successfully")


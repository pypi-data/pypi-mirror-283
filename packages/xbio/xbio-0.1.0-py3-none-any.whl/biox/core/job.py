from typing import List, Optional, Callable, Dict, Union

from biox.core.command import Command
from biox.core.log import LoggingMixin
from biox.core.status import Status


class Job(LoggingMixin):
    def __init__(
        self,
        job_name: str,
        cmd: Callable[..., Command],
        job_input_dir: Optional[str] = None,
        job_output_dir: Optional[str] = None,
        env: Optional[dict] = None,
        deps: Optional[List[str]] = None,
        inputs: Optional[Union[List[Dict[str, str]], str]] = None,
        outputs: Optional[Union[List[Dict[str, str]], str]] = None,
    ):
        self._commands: List[Command] = []
        self.cmd = cmd
        self._job_name = job_name
        self._job_input_dir = job_input_dir
        self._job_output_dir = job_output_dir
        self._deps = deps or []
        self._env = env or {}
        self._status: Status = Status.PENDING
        self.inputs = inputs
        self.outputs = outputs
        self.stdins: List[str] = []
        self.stdout: Optional[str] = None

    def _handle_cmd(self, cmd: Union[Callable[..., Command], str]):
        pass

    def map(
        self,
        inputs: List[Dict[str, str]],
    ):
        commands = []
        for index, template_date in enumerate(inputs, start=len(self._commands)):
            c = self.eat(index, template_date)
            commands.append(c)
        return commands

    def eat(self, command_id: int, input: Dict[str, str]):
        cmd = self.cmd(**input)
        cmd.set_command_id(command_id)
        self._commands.append(cmd)
        return cmd

    def __str__(self):
        return self.commands

    @property
    def commands(self) -> List[Command]:
        return self._commands

    @property
    def job_name(self):
        return self._job_name

    @property
    def env(self):
        return self._env

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

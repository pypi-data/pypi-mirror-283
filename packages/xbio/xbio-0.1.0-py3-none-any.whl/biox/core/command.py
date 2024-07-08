from typing import Callable, Dict, Optional

from biox.core.log import LoggingMixin
from biox.core.binary import get_binary_path
from biox.core.status import Status
from biox.core.util import get_function_parameters


class Command(LoggingMixin):
    def __init__(
        self,
        command_name: str,
        command_description: str,
        command_template: str,
        template_data: Dict[str, str],
    ):
        self._command_id = -1
        self._command_name: str = command_name
        self._command_description: str = command_description
        self._binary: str = ""
        self.__command: str = ""
        self._command_template = command_template
        self._status: Status = Status.PENDING
        self._template_data = template_data
        self.__post_init__()

    def __post_init__(self):
        binary, command_template = self._command_template.split(" ", 1)
        binary_path = get_binary_path(binary)
        if binary_path is None:
            raise FileNotFoundError(f"Binary {binary} not found")
        self._binary = binary_path.absolute().as_posix()
        self._command_template = f"{self._binary} {command_template}"

    def set_command_id(self, command_id: int):
        self._command_id = command_id

    @property
    def command_name(self):
        return self._command_name

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: Status):
        self._status = value

    @property
    def command_id(self):
        return self._command_id

    @command_id.setter
    def command_id(self, value: int):
        self._command_id = value

    @property
    def binary(self):
        return self._binary

    @property
    def command(self):
        if not self.__command:
            self.__command = self._command_template.format(**self._template_data)
        return self.__command

    @property
    def command_template(self):
        return self._command_template

    def __str__(self):
        return self.command

    def __repr__(self):
        return f"<command:{self.command_name} {self.command}>"

    def json(self):
        return {
            "binary": self._binary,
            "command": self.command,
            "status": self._status.value,
            "template": self._command_template,
            "template_kwargs": self._template_data,
            "name": self.command_name,
            "description": self._command_description,
        }


def command(
    command_template: str,
    command_name: Optional[str] = None,
    command_description: Optional[str] = None,
) -> Callable[..., Callable[..., Command]]:
    def decorator(func: Callable):
        def wrapper(*args, **default_template_kwargs):
            template_kwargs = {}
            parameters = get_function_parameters(func)
            args_names = list(parameters.keys())
            for args_name in args_names:
                parameter = parameters[args_name]
                if parameter.default is not parameter.empty:
                    template_kwargs[parameter.name] = parameter.default

            template_kwargs.update(default_template_kwargs)
            if len(args) > 0:
                for i, arg in enumerate(args):
                    template_kwargs[args_names[i]] = arg
            keys1 = set(template_kwargs.keys())
            keys2 = set(parameters.keys())
            assert keys1 & keys2 == keys2, f"Missing values for {keys2 - keys1}"
            command = Command(
                command_name=command_name or func.__name__,
                command_description=command_description or func.__doc__ or "",
                command_template=command_template,
                template_data=template_kwargs,
            )
            command.__class__.__name__ = command_name or func.__name__
            return command

        return wrapper

    return decorator

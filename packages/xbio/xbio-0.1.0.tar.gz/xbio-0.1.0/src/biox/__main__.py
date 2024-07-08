from biox.core.command import command
from biox.core.workflow import Workflow
from biox.core.execute import ShellExecutor
from biox.core.binary import BinaryManager
from biox.core.dataset import DatasetManager


class Input:

    def __init__(self, *args, **kwargs):
        ...

    @classmethod
    def __class_getitem__(cls, item):
        ...

class Output:

    def __init__(self, *args, **kwargs):
        ...


@command(
    command_template="echo {message}, $a",
)
def echo(message: Input[str]):
    r"""ssssssssssssssssssssssssssssss"""
    return Output(message=message)

job1_inputs = [
    {"message": i}
    for i in [
        "Hello",
        "World",
        "This is a test",
    ]
]

w = Workflow()

w.add_job(
    job_name="job2",
    cmd=echo,
    env={"a": "bbbbbbbbb"},
)

w.add_job(
    job_name="job1",
    cmd=echo,
    job_input_dir="data",
    job_output_dir="output",
    env={"a": "b"},
    deps=["job2"],
    inputs="job2.outputs",
)



from rich import print
w.execute()
w.add_job(
    job_name="job3",
    cmd=echo,
    job_input_dir="data",
    job_output_dir="output",
    inputs="job2.inputs",
)
print(w.inputs())
print(w.inputs("job1"))

w.execute()


print(w.debug())

import time
import typing
from collections import OrderedDict
from typing import Dict, List, Optional
import copy

from biox.core.job import Job
from biox.core.command import Command
from biox.core.log import LoggingMixin
from biox.core.status import Status
from biox.core.binary import BinaryManager
from biox.core.dataset import DatasetManager
from biox.core.execute import ExecuteABC


__all__ = ["Workflow", "execute"]


class CycleError(Exception):
    pass


class DAG:
    def __init__(self):
        self._dag: typing.OrderedDict[str, List[str]] = OrderedDict()

    def _detect_cycle(self):
        dag = copy.deepcopy(self._dag)
        q = []
        for k, v in dag.items():
            if len(v) == 0:
                q.append(k)
        while q:
            node = q.pop(0)
            for k, v in dag.items():
                if node in v:
                    v.remove(node)
                    if len(v) == 0:
                        q.append(k)
            dag.pop(node)
        if len(dag) != 0:
            raise CycleError("Cycle detected")

    def add_job(self, job_name: str, job: Job):
        if job_name not in self._dag:
            self._dag[job_name] = []
        for dep in job._deps:
            if dep not in self._dag:
                self._dag[dep] = []
            self._dag[dep].append(job_name)
        self._detect_cycle()

        return self

    def topo_sort(self):
        dag = copy.deepcopy(self._dag)
        sorted_jobs = []
        q = []
        for k, v in dag.items():
            if len(v) == 0:
                q.append(k)
        while q:
            node = q.pop(0)
            sorted_jobs.append(node)
            for k, v in dag.items():
                if node in v:
                    v.remove(node)
                    if len(v) == 0:
                        q.append(k)
            dag.pop(node)
        return sorted_jobs[::-1]


class Workflow(LoggingMixin):
    def __init__(
        self,
        name: str = "Biox",
        description: str = "A bioinformatics workflow manager",
        author: str = "Biox",
        version: str = "0.1",
        debug_mode: bool = True,
    ):
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.debug_mode = debug_mode
        self._jobs: Dict[str, Job] = {}
        self._dag = DAG()
        self._execute: Optional[ExecuteABC] = None
        self._binary_manager: Optional[BinaryManager] = None
        self._dataset_manager = DatasetManager()

    def set_execute(self, execute: ExecuteABC):
        self._execute = execute
        return self

    def set_binary_manager(self, binary_manager: BinaryManager):
        self._binary_manager = binary_manager
        return self





    def add_job(
        self,
        job_name: str,
        cmd: typing.Callable[..., Command],
        job_input_dir: typing.Optional[str] = None,
        job_output_dir: typing.Optional[str] = None,
        env: typing.Optional[dict] = None,
        deps: typing.Optional[List[str]] = None,
        inputs: typing.Optional[typing.Union[List[Dict[str, str]], str]] = None,
        outputs: typing.Optional[typing.Union[List[Dict[str, str]], str]] = None,
    ):
        job = Job(
            job_name=job_name,
            cmd=cmd,
            job_input_dir=job_input_dir,
            job_output_dir=job_output_dir,
            env=env,
            deps=deps,
            inputs=inputs,
            outputs=outputs,
        )
        if job.job_name in self._jobs:
            raise ValueError(f"Job {job.job_name} already exists")
        try:
            self._dag.add_job(job.job_name, job)
        except CycleError:
            self.log.error(f"Cycle detected in job {job.job_name}")
            exit(1)
        self._jobs[job.job_name] = job
        return self

    def _fill_inputs_and_outputs(self):
        sorted_jobs = self._dag.topo_sort()
        for job_name in sorted_jobs:
            if job_name not in self._jobs:
                raise ValueError(f"Job {job_name} not found")
            job = self._jobs[job_name]
            inputs = []
            outputs = []

            if isinstance(job.inputs, list):
                inputs = job.inputs
                self._dataset_manager.send_input(job.job_name, inputs)
                job.inputs = inputs

            elif isinstance(job.inputs, str):
                job_name, type = job.inputs.split(".")
                type = type.lower()
                if "input" in type:
                    inputs = self._dataset_manager.get_input(job_name)
                elif "output" in type:
                    inputs = self._dataset_manager.get_output(job_name)
                self._dataset_manager.send_input(job.job_name, inputs)
                job.inputs = inputs

            else:
                inputs = self._dataset_manager.get_input(job.job_name)
                job.inputs = inputs

            if isinstance(job.outputs, list):
                outputs = job.outputs
                self._dataset_manager.send_output(job.job_name, outputs)
                job.outputs = outputs

            elif isinstance(job.outputs, str):
                job_name, type = job.outputs.split(".")
                type = type.lower()
                if "input" in type:
                    outputs = self._dataset_manager.get_input(job_name)
                elif "output" in type:
                    outputs = self._dataset_manager.get_output(job_name)

                self._dataset_manager.send_output(job.job_name, outputs)
                job.outputs = outputs

            else:
                outputs = self._dataset_manager.get_output(job.job_name)
                job.outputs = outputs

    def __str__(self):
        return self._jobs

    def execute(self):
        self.log.info("Executing workflow")
        self._fill_inputs_and_outputs()
        jobs = self._dag.topo_sort()

        for job_name in jobs:
            job = self._jobs[job_name]
            if job.status == Status.COMPLETED:
                continue
            inputs = self._dataset_manager.get_input(job_name)
            job.map(inputs)
            count = 1
            while True:
                if (not job._deps) or all(
                    [self._jobs[dep].status == Status.COMPLETED for dep in job._deps]
                ):
                    break
                time.sleep(0.5 * count)
                count += 1
                if count > 20:
                    count = 1
                self.log.info(
                    f"{job.job_name.capitalize()} is waiting for dependencies of job {job._deps}"
                )
            self.log.info(f"Executing job {job_name}")
            assert (
                self._execute is not None
            ), "Execute object is not set, run _set_execute first"
            self._execute.execute_job(job)
            self.log.info(f"Job {job_name} completed")
        self.log.info("Workflow completed")

    def inputs(self, job_name: Optional[str] = None):
        self._fill_inputs_and_outputs()
        if job_name is None:
            return self._dataset_manager.inputs
        d = self._dataset_manager.get_input(job_name)
        return {job_name: d}

    def outputs(self, job_name: Optional[str] = None):
        self._fill_inputs_and_outputs()
        if job_name is None:
            return self._dataset_manager.outputs
        d = self._dataset_manager.get_output(job_name)
        return {job_name: d}

    def debug(self) -> Dict[str, List[str]]:
        self._fill_inputs_and_outputs()
        jobs = self._dag.topo_sort()
        d = {}
        for job_name in jobs:
            job = self._jobs[job_name]
            inputs = self._dataset_manager.get_input(job_name)
            job.map(inputs)
            d[job_name] = [c.command for c in job.commands]
        return d



def execute():
    pass

from __future__ import annotations
import typing

from everai.utils.size import from_human_size, human_size_number
from generated.apps import V1Resource, V1ResourceFilter


class ResourceRequests:
    cpu_num: int
    gpu_num: int
    memory_mb: int

    region_constraints: typing.List[str]
    cpu_constraints: typing.List[str]
    gpu_constraints: typing.List[str]

    driver_version_constraints: typing.Optional[str]
    cuda_version_constraints: typing.Optional[str]

    def __init__(self, cpu_num: int = 1, memory_mb: int = 1024, gpu_num: int = 0,
                 region_constraints: typing.List[str] = None,
                 cpu_constraints: typing.List[str] = None,
                 gpu_constraints: typing.List[str] = None,
                 driver_version_constraints: typing.Optional[str] = None,
                 cuda_version_constraints: typing.Optional[str] = None,
                 ):
        """
        :param cpu_num: Number of CPU, default is 1
        :param gpu_num: Number of GPU, default is 0
        :param memory_mb: Memory size in MB, default is 1024
        :param region_constraints: Region constraints, default is any region
        :param cpu_constraints: Cpu constraints, default is any cpu type
        :param gpu_constraints: Gpu constraints, default is any gpu type
        :param driver_version_constraints: Driver version constraints, default is any version， e.g. >=535.154.05
        :param cuda_version_constraints: Cuda version constraints, default is any version, e.g. >=12.2
        """
        assert cpu_num > 0, "cpu_num must be positive"
        assert gpu_num >= 0
        assert memory_mb > 0, "memory_mb must be positive"

        self.cpu_num = cpu_num
        self.gpu_num = gpu_num
        self.memory_mb = memory_mb

        self.region_constraints = region_constraints
        self.cpu_constraints = cpu_constraints
        self.gpu_constraints = gpu_constraints
        self.driver_version_constraints = driver_version_constraints
        self.cuda_version_constraints = cuda_version_constraints

    def to_proto(self) -> V1Resource:
        filters = V1ResourceFilter(
            gpu=self.gpu_constraints,
            cpu=self.cpu_constraints,
            regions=self.region_constraints,
            cuda=self.cuda_version_constraints,
            nvidia=self.driver_version_constraints,
        )
        if (
                (self.gpu_constraints is None or len(self.gpu_constraints) == 0) and
                (self.cpu_constraints is None or len(self.cpu_constraints) == 0) and
                (self.region_constraints is None or len(self.region_constraints) == 0) and
                self.cuda_version_constraints is None and self.driver_version_constraints is None
        ):
            filters = None
        return V1Resource(
            cpu=self.cpu_num,
            gpu=None if self.gpu_num is None or self.gpu_num == 0 else self.gpu_num,
            memory=f'{self.memory_mb} MiB',
            filters=filters,
        )

    @staticmethod
    def from_proto(resource: V1Resource) -> ResourceRequests:
        return ResourceRequests(
            cpu_num=resource.cpu,
            gpu_num=resource.gpu,
            memory_mb=int(human_size_number(from_human_size(resource.memory), "MiB")),
            gpu_constraints=resource.filters.gpu,
            cpu_constraints=resource.filters.cpu,
            region_constraints=resource.filters.regions,
            cuda_version_constraints=resource.filters.cuda,
            driver_version_constraints=resource.filters.nvidia
        )

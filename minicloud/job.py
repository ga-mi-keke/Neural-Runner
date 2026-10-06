from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Job:
    id: str
    command: list[str]
    status: str = "pending"


def create_job(command: list[str]) -> Job:
    return Job(
        id=str(uuid4()),
        command=command,
    )
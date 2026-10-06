from dataclasses import dataclass
import subprocess

from job import Job


@dataclass
class JobResult:
    status: str
    return_code: int | None
    stdout: str
    stderr: str


def run_job(job: Job, timeout: float = 10.0) -> JobResult:
    job.status = "running"

    try:
        completed = subprocess.run(
            job.command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        job.status = (
            "succeeded"
            if completed.returncode == 0
            else "failed"
        )

        return JobResult(
            status=job.status,
            return_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    except subprocess.TimeoutExpired as e:
        job.status = "timed_out"

        return JobResult(
            status=job.status,
            return_code=None,
            stdout=e.stdout or "",
            stderr=e.stderr or "",
        )
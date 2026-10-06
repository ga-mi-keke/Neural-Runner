from queue import Queue
from threading import Thread

from job import Job, create_job
from runner import run_job


class JobManager:
    def __init__(self, worker_count: int = 2):
        self.jobs: dict[str, Job] = {}
        self.queue: Queue[Job | None] = Queue()
        self.workers: list[Thread] = []

        for _ in range(worker_count):
            worker = Thread(target=self._worker)
            worker.start()

            self.workers.append(worker)

    def submit(self, command: list[str]) -> Job:
        job = create_job(command)

        self.jobs[job.id] = job
        self.queue.put(job)

        return job

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def _worker(self):
        while True:
            job = self.queue.get()

            if job is None:
                self.queue.task_done()
                break

            run_job(job)

            self.queue.task_done()

    def shutdown(self):
        for _ in self.workers:
            self.queue.put(None)

        for worker in self.workers:
            worker.join()

    def list_jobs(self) -> list[Job]:
        return list(self.jobs.values())
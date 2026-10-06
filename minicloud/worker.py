from threading import Thread
from queue import Queue

from job import Job
from runner import run_job


class Worker:
    def __init__(self, worker_id: str):
        self.id = worker_id
        self.status = "idle"
        self.queue: Queue[Job | None] = Queue()

        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while True:
            job = self.queue.get()

            if job is None:
                break

            self.status = "busy"

            run_job(job)

            self.status = "idle"

    def assign(self, job: Job):
        self.queue.put(job)

    def shutdown(self):
        self.queue.put(None)
        self.thread.join()
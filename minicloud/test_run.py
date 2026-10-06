import time

from manager import JobManager


manager = JobManager(worker_count=2)

jobs = []

for i in range(4):
    job = manager.submit([
        "python",
        "-c",
        f"import time; time.sleep(3); print('job {i}')"
    ])

    jobs.append(job)

time.sleep(1)

for job in jobs:
    print(job.status)

time .sleep(4)

for job in jobs:
    print(job.status)
manager.shutdown()
import json
import socket
from threading import Thread

from manager import JobManager


manager = JobManager(worker_count=2)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8000))
server.listen()

client_threads: list[Thread] = []

print("MiniCloud server started")


def handle_client(conn, address):
    try:
        data = conn.recv(1024)
        request = json.loads(data.decode())

        job = manager.submit(request["command"])

        response = {
            "job_id": job.id,
            "status": job.status,
        }

        conn.sendall(json.dumps(response).encode())

    finally:
        conn.close()


try:
    while True:
        conn, address = server.accept()

        thread = Thread(
            target=handle_client,
            args=(conn, address),
        )

        thread.start()
        client_threads.append(thread)

except KeyboardInterrupt:
    print("MiniCloud shutting down")

finally:
    server.close()

    for thread in client_threads:
        thread.join()

    manager.shutdown()
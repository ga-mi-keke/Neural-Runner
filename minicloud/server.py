import json
import socket
from dataclasses import asdict
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
        data = conn.recv(4096)
        request_text = data.decode()

        header_text, body = request_text.split("\r\n\r\n", 1)

        header_lines = header_text.split("\r\n")

        request_line = header_lines[0]
        method, path, version = request_line.split(" ")

        headers = {}

        for line in header_lines[1:]:
            key, value = line.split(": ", 1)
            headers[key] = value

        content_length = int(headers.get("Content-Length", 0))

        if method == "GET" and path == "/jobs":
            jobs = manager.list_jobs()

            job_data = []

            for job in jobs:
                job_data.append(asdict(job))

            body = json.dumps(job_data)

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(body)}\r\n"
                "\r\n"
                f"{body}"
            )
        elif method == "POST" and path == "/jobs":
            request_data = json.loads(body)

            job = manager.submit(request_data["command"])

            response_data = {
                "job_id": job.id,
                "status": job.status,
            }

            body = json.dumps(response_data)

            response = (
                "HTTP/1.1 201 Created\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(body)}\r\n"
                "\r\n"
                f"{body}"
            )

        else:
            body = "Not Found"

            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(body)}\r\n"
                "\r\n"
                f"{body}"
            )

        conn.sendall(response.encode())

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
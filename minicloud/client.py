import json
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8000))

request = {
    "command": ["python", "-c", "print('Hello MiniCloud')"]
}

data = json.dumps(request).encode()

client.sendall(data)

response = client.recv(1024)
print(response.decode())

client.close()
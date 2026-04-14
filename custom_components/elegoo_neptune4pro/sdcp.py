
import json, socket

class SDCPClient:
    def __init__(self, host, port=3000):
        self.host = host
        self.port = port

    def send(self, payload):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(json.dumps(payload).encode(), (self.host, self.port))
        data, _ = sock.recvfrom(4096)
        return json.loads(data.decode())

    def status(self):
        return self.send({"cmd": "status"})

    def pause(self):
        self.send({"cmd": "pause"})

    def resume(self):
        self.send({"cmd": "resume"})

    def stop(self):
        self.send({"cmd": "stop"})

    def set_temp(self, tool, value):
        self.send({"cmd": "set_temp", "tool": tool, "value": value})

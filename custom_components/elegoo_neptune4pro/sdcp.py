
# Minimal SDCP client (UDP)
import socket, json

class SDCPClient:
    def __init__(self, host, port=3000):
        self.host = host
        self.port = port

    def _send(self, payload):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.sendto(json.dumps(payload).encode(), (self.host, self.port))
        data, _ = s.recvfrom(8192)
        return json.loads(data.decode())

    def status(self):
        return self._send({"cmd": "status"})

    def pause(self): self._send({"cmd": "pause"})
    def resume(self): self._send({"cmd": "resume"})
    def stop(self): self._send({"cmd": "stop"})
    def set_temp(self, tool, val):
        self._send({"cmd": "set_temp", "tool": tool, "value": val})

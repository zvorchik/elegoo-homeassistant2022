import socket, json

class SDCPClient:
    def __init__(self, host, port=3000):
        self.host = host
        self.port = port

    def _send(self, payload):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(json.dumps(payload).encode(), (self.host, self.port))
        data, _ = sock.recvfrom(8192)
        return json.loads(data.decode())

    def status(self): return self._send({'cmd': 'status'})
    def pause(self): self._send({'cmd': 'pause'})
    def resume(self): self._send({'cmd': 'resume'})
    def stop(self): self._send({'cmd': 'stop'})
    def set_temp(self, tool, value): self._send({'cmd': 'set_temp', 'tool': tool, 'value': value})

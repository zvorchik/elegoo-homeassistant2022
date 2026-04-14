
from homeassistant.components.camera import Camera

class ElegooCamera(Camera):
    def __init__(self, host):
        super().__init__()
        self.host = host

    def camera_image(self, **kwargs):
        import requests
        return requests.get(f"http://{self.host}:8080/?action=snapshot", timeout=5).content

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ElegooCamera(entry.data['host'])])

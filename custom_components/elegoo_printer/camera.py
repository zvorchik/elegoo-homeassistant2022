
from homeassistant.components.camera import Camera
import requests

class ElegooCamera(Camera):
    def __init__(self, host): self.host = host; super().__init__()
    def camera_image(self, **kw):
        return requests.get(f"http://{self.host}:8080/?action=snapshot", timeout=5).content

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ElegooCamera(entry.data['host'])])

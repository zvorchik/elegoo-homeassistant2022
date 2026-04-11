from homeassistant.components.camera import Camera
from .const import DOMAIN

class MoonrakerCamera(Camera):
    def __init__(self, host): super().__init__(); self.host=host
    def camera_image(self, **kw):
        import requests
        return requests.get(f"http://{self.host}:7125/webcam/?action=snapshot",timeout=5).content

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([MoonrakerCamera(entry.data['host'])])

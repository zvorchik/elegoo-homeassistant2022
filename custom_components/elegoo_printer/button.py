from homeassistant.components.button import ButtonEntity
import requests

class MoonrakerButton(ButtonEntity):
    def __init__(self, host, name, cmd): self._attr_name=name; self.host=host; self.cmd=cmd
    def press(self): requests.post(f"http://{self.host}:7125/printer/print/{self.cmd}")

async def async_setup_entry(hass, entry, async_add_entities):
    h=entry.data['host']
    async_add_entities([
        MoonrakerButton(h,'Pause Print','pause'),
        MoonrakerButton(h,'Resume Print','resume'),
        MoonrakerButton(h,'Stop Print','cancel'),
    ])

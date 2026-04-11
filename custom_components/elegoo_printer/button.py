from homeassistant.components.button import ButtonEntity
import requests

class ElegooButton(ButtonEntity):
    def __init__(self, host, name, cmd):
        self.host = host
        self.cmd = cmd
        self._attr_name = name

    def press(self):
        requests.post(f"http://{self.host}:7125/printer/print/{self.cmd}")

async def async_setup_entry(hass, entry, async_add_entities):
    h = entry.data['host']
    async_add_entities([
        ElegooButton(h, 'Pause Print', 'pause'),
        ElegooButton(h, 'Resume Print', 'resume'),
        ElegooButton(h, 'Stop Print', 'cancel'),
    ])

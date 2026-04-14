
from homeassistant.components.number import NumberEntity
import requests

class TempNumber(NumberEntity):
    def __init__(self, host, name, cmd, min_v, max_v):
        self.host = host
        self.cmd = cmd
        self._attr_name = name
        self._attr_min_value = min_v
        self._attr_max_value = max_v

    def set_native_value(self, value):
        requests.post(f"http://{self.host}:7125/printer/gcode/script", json={"script": self.cmd.format(value)})

async def async_setup_entry(hass, entry, async_add_entities):
    h = entry.data['host']
    async_add_entities([
        TempNumber(h, "Set Nozzle Temp", "M104 S{}", 0, 300),
        TempNumber(h, "Set Bed Temp", "M140 S{}", 0, 120)
    ])

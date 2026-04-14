
from homeassistant.components.number import NumberEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        TempNumber(c, "Nozzle Temp", "nozzle", 0, 300),
        TempNumber(c, "Bed Temp", "bed", 0, 120),
    ])

class TempNumber(NumberEntity):
    def __init__(self, client, name, tool, minv, maxv):
        self.client = client
        self.tool = tool
        self._attr_name = name
        self._attr_min_value = minv
        self._attr_max_value = maxv

    def set_native_value(self, value):
        self.client.set_temp(self.tool, int(value))

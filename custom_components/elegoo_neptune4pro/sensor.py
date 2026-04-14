
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

SENS = {
    'state': 'State',
    'progress': 'Progress',
    'nozzle': 'Nozzle Temp',
    'bed': 'Bed Temp',
}

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ElegooSensor(client, entry, k, name)
        for k, name in SENS.items()
    ], True)

class ElegooSensor(SensorEntity):
    def __init__(self, client, entry, key, name):
        self.client = client
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Elegoo Printer",
            manufacturer="Elegoo",
            model="Neptune 4 Pro",
        )

    async def async_update(self):
        d = self.client.status()
        self._attr_native_value = d.get(self.key)

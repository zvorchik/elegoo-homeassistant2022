from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ElegooSensor(c, entry, 'state', 'State'),
        ElegooSensor(c, entry, 'progress', 'Progress'),
        ElegooSensor(c, entry, 'nozzle', 'Nozzle Temp'),
        ElegooSensor(c, entry, 'bed', 'Bed Temp'),
    ], True)

class ElegooSensor(SensorEntity):
    def __init__(self, client, entry, key, name):
        self.client = client
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name='Elegoo Printer',
            manufacturer='Elegoo',
            model='Neptune 4 Plus'
        )

    async def async_update(self):
        self._attr_native_value = self.client.status().get(self.key)

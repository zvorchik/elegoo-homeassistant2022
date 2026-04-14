
from homeassistant.components.sensor import SensorEntity
from .sdcp import SDCPClient

async def async_setup_entry(hass, entry, async_add_entities):
    client = SDCPClient(entry.data['host'])
    async_add_entities([
        ElegooSensor(client, 'state'),
        ElegooSensor(client, 'progress'),
        ElegooSensor(client, 'nozzle'),
        ElegooSensor(client, 'bed'),
    ], True)

class ElegooSensor(SensorEntity):
    def __init__(self, client, kind):
        self.client = client
        self.kind = kind
        self._attr_name = f"Elegoo {kind}"

    async def async_update(self):
        data = self.client.status()
        self._attr_native_value = data.get(self.kind)

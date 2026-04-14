
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

SENSORS = {
    "state": ("Print State", lambda d: d['print_stats']['state']),
    "progress": ("Progress %", lambda d: round(d['display_status']['progress'] * 100, 1)),
    "nozzle": ("Nozzle Temp", lambda d: d['extruder']['temperature']),
    "bed": ("Bed Temp", lambda d: d['heater_bed']['temperature']),
}

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ElegooSensor(entry.data['host'], k, v[0], v[1]) for k, v in SENSORS.items()], True)

class ElegooSensor(SensorEntity):
    def __init__(self, host, key, name, fn):
        self.host = host
        self._fn = fn
        self._attr_name = name
        self._attr_unique_id = f"elegoo_{key}_{host}"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, host)}, name="Elegoo Printer", manufacturer="Elegoo", model="Neptune 4 Pro")

    async def async_update(self):
        async with aiohttp.ClientSession() as s:
            async with s.get(f"http://{self.host}:7125/printer/objects/query?print_stats&display_status&extruder&heater_bed") as r:
                js = await r.json()
                self._attr_native_value = self._fn(js['result']['status'])

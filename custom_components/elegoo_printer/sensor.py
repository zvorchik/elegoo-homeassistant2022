
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        PrinterState(entry),
        PrinterProgress(entry),
        NozzleTemp(entry),
        BedTemp(entry),
    ], True)

class BaseMoonrakerSensor(SensorEntity):
    def __init__(self, entry):
        self.host = entry.data['host']
        self._attr_device_info = DeviceInfo(
            identifiers={("elegoo", self.host)},
            name="Elegoo Printer",
            manufacturer="Elegoo",
            model="Neptune 4 / 4 Plus",
        )

    async def _get(self):
        async with aiohttp.ClientSession() as s:
            async with s.get(f"http://{self.host}:7125/printer/objects/query?print_stats&display_status&extruder&heater_bed") as r:
                return (await r.json())['result']['status']

class PrinterState(BaseMoonrakerSensor):
    _attr_name = 'Printer State'
    async def async_update(self): self._attr_native_value = (await self._get())['print_stats']['state']

class PrinterProgress(BaseMoonrakerSensor):
    _attr_name = 'Print Progress'
    async def async_update(self): self._attr_native_value = round((await self._get())['display_status']['progress']*100,1)

class NozzleTemp(BaseMoonrakerSensor):
    _attr_name = 'Nozzle Temperature'
    async def async_update(self): self._attr_native_value = (await self._get())['extruder']['temperature']

class BedTemp(BaseMoonrakerSensor):
    _attr_name = 'Bed Temperature'
    async def async_update(self): self._attr_native_value = (await self._get())['heater_bed']['temperature']

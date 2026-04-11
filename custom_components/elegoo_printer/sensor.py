from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import MoonrakerCoordinator
from .const import DOMAIN

SENSORS = {
    "status": ("Print Status", lambda d: d['print_stats']['state']),
    "progress": ("Progress %", lambda d: round(d['display_status']['progress'] * 100, 1)),
    "nozzle": ("Nozzle Temp", lambda d: d['extruder']['temperature']),
    "bed": ("Bed Temp", lambda d: d['heater_bed']['temperature'])
}

async def async_setup_entry(hass, entry, async_add_entities):
    coord = MoonrakerCoordinator(hass, entry.data['host'])
    await coord.async_config_entry_first_refresh()
    async_add_entities([ElegooSensor(coord, name, func) for name, (_, func) in SENSORS.items()])

class ElegooSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, fn):
        super().__init__(coordinator)
        self._attr_name = name
        self.fn = fn

    @property
    def native_value(self):
        return self.fn(self.coordinator.data)

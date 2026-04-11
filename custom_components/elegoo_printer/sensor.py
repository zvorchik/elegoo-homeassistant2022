from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import MoonrakerCoordinator

SENSORS = {
    "Print Status": lambda d: d['print_stats']['state'],
    "Progress %": lambda d: round(d['display_status']['progress'] * 100, 1),
    "Nozzle Temp": lambda d: d['extruder']['temperature'],
    "Bed Temp": lambda d: d['heater_bed']['temperature'],
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = MoonrakerCoordinator(hass, entry.data['host'])
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([
        ElegooSensor(coordinator, name, fn) for name, fn in SENSORS.items()
    ])

class ElegooSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, fn):
        super().__init__(coordinator)
        self._attr_name = name
        self._fn = fn

    @property
    def native_value(self):
        return self._fn(self.coordinator.data)

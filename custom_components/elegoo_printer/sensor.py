from homeassistant.components.sensor import SensorEntity
from .coordinator import MoonrakerCoordinator
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

SENSORS = {
  "state": ("Print Status", lambda d:d['print_stats']['state']),
  "progress": ("Progress %", lambda d:round(d['display_status']['progress']*100,1)),
  "nozzle": ("Nozzle Temp", lambda d:d['extruder']['temperature']),
  "bed": ("Bed Temp", lambda d:d['heater_bed']['temperature']),
  "speed": ("Print Speed", lambda d:d['toolhead']['estimated_print_time']),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coord=MoonrakerCoordinator(hass, entry.data['host'])
    await coord.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN,{})[entry.entry_id]=coord
    async_add_entities([ElegooSensor(coord,k,n,f) for k,(n,f) in SENSORS.items()])

class ElegooSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coord,key,name,fn):
        super().__init__(coord)
        self._attr_name=name
        self.key=key; self.fn=fn
    @property
    def native_value(self): return self.fn(self.coordinator.data)

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([PrinterStatusSensor(entry.data['host'])])

class PrinterStatusSensor(SensorEntity):
    def __init__(self, host):
        self._attr_name = "Printer Status"
        self._attr_unique_id = f"elegoo_neptune4pro_status_{host}"
        self._state = "online"
        self.host = host

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={("elegoo_neptune4pro", self.host)},
            name="Elegoo Neptune 4 Pro",
            manufacturer="Elegoo",
            model="Neptune 4 Pro",
        )

    @property
    def native_value(self):
        return self._state

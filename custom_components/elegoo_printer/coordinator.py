from datetime import timedelta
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

class MoonrakerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host):
        self.host=host
        super().__init__(hass, None, name="Moonraker", update_interval=timedelta(seconds=3))
    async def _async_update_data(self):
        url=f"http://{self.host}:7125/printer/objects/query?print_stats&display_status&extruder&heater_bed&toolhead&fan"
        async with aiohttp.ClientSession() as s:
            async with s.get(url,timeout=5) as r:
                if r.status!=200: raise UpdateFailed("Moonraker error")
                return (await r.json())['result']['status']

from datetime import timedelta
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class MoonrakerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host):
        self.host = host
        super().__init__(hass, None, name="Moonraker", update_interval=timedelta(seconds=3))

    async def _async_update_data(self):
        url = f"http://{self.host}:7125/printer/objects/query?print_stats&display_status&extruder&heater_bed"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                data = await resp.json()
                return data['result']['status']

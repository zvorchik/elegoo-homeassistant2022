
from .const import DOMAIN
from .sdcp import SDCPClient

async def async_setup_entry(hass, entry):
    client = SDCPClient(entry.data['host'])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "button")
    await hass.config_entries.async_forward_entry_setup(entry, "number")
    await hass.config_entries.async_forward_entry_setup(entry, "camera")
    return True

async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True

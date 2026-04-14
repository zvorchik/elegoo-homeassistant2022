
async def async_setup_entry(hass, entry):
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "button")
    return True

async def async_unload_entry(hass, entry):
    return True

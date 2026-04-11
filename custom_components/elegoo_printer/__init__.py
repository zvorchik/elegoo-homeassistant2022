from .const import DOMAIN

PLATFORMS = ["sensor", "camera", "button"]

async def async_setup_entry(hass, entry):
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True

async def async_unload_entry(hass, entry):
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_unload(entry, platform)
        )
    return True

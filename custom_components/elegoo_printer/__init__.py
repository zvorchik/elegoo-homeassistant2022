
DOMAIN = 'elegoo_printer'

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    await hass.config_entries.async_forward_entry_setup(entry, 'sensor')
    await hass.config_entries.async_forward_entry_setup(entry, 'camera')
    await hass.config_entries.async_forward_entry_setup(entry, 'button')
    return True

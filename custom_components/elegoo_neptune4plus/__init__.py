DOMAIN = "elegoo_neptune4plus"

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    # ІМПОРТ ТІЛЬКИ ТУТ
    from .sdcp import SDCPClient

    client = SDCPClient(entry.data["host"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "button")
    await hass.config_entries.async_forward_entry_setup(entry, "number")
    await hass.config_entries.async_forward_entry_setup(entry, "camera")
    return True
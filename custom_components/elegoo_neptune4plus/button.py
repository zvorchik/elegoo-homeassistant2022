from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ActionButton(c, 'Pause', 'pause'),
        ActionButton(c, 'Resume', 'resume'),
        ActionButton(c, 'Stop', 'stop'),
    ])

class ActionButton(ButtonEntity):
    def __init__(self, client, name, cmd):
        self.client = client
        self._attr_name = name
        self.cmd = cmd
    def press(self): getattr(self.client, self.cmd)()

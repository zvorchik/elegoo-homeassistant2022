
from homeassistant.components.button import ButtonEntity
from .sdcp import SDCPClient

async def async_setup_entry(hass, entry, async_add_entities):
    client = SDCPClient(entry.data['host'])
    async_add_entities([
        ElegooButton(client, 'Pause', 'pause'),
        ElegooButton(client, 'Resume', 'resume'),
        ElegooButton(client, 'Stop', 'stop'),
    ])

class ElegooButton(ButtonEntity):
    def __init__(self, client, name, cmd):
        self.client = client
        self._attr_name = name
        self.cmd = cmd

    def press(self):
        getattr(self.client, self.cmd)()

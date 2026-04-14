
import requests
from homeassistant.components.button import ButtonEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        PauseButton(entry), ResumeButton(entry), CancelButton(entry),
        FlashlightButton(entry), ModelLightButton(entry),
    ])

class BaseButton(ButtonEntity):
    def __init__(self, entry): self.host = entry.data['host']

class PauseButton(BaseButton):
    _attr_name = 'Pause Print'
    def press(self): requests.post(f"http://{self.host}:7125/printer/print/pause")

class ResumeButton(BaseButton):
    _attr_name = 'Resume Print'
    def press(self): requests.post(f"http://{self.host}:7125/printer/print/resume")

class CancelButton(BaseButton):
    _attr_name = 'Cancel Print'
    def press(self): requests.post(f"http://{self.host}:7125/printer/print/cancel")

class FlashlightButton(BaseButton):
    _attr_name = 'Hotend LED'
    def press(self): requests.post(f"http://{self.host}:7125/printer/gcode/script", json={'script':'FLASHLIGHT_SWITCH'})

class ModelLightButton(BaseButton):
    _attr_name = 'Logo LED'
    def press(self): requests.post(f"http://{self.host}:7125/printer/gcode/script", json={'script':'MODLELIGHT_SWITCH'})

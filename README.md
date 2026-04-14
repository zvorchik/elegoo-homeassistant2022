
# Elegoo Neptune 4 Pro – MAX integration (no Moonraker, HA 2022.5.5)

This integration is based on the **Elegoo SDCP protocol**, adapted from the original
`danielcherubini/elegoo-homeassistant` architecture, but rewritten to be compatible
with **Home Assistant 2022.5.5** and **stock Elegoo firmware**.

## Features
- Printer device appears correctly
- Sensors: state, progress, nozzle temp, bed temp
- Buttons: pause / resume / stop
- Set temperatures (nozzle / bed)
- Camera via MJPEG endpoint (iframe-compatible)

NO Moonraker. NO port 7125.

## Installation
Copy `custom_components/elegoo_neptune4pro` to `/config/custom_components`
then FULL reboot and add integration **Elegoo Printer**.

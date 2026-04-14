
Elegoo Neptune 4 Plus – Home Assistant integration (SDCP, no Moonraker)

This is a FULL, WORKING base for Elegoo Neptune 4 Plus using stock firmware.
Home Assistant: tested concept for 2022.5.5 architecture.

Features:
- Proper device creation
- Sensors: state, progress, nozzle temp, bed temp
- Buttons: pause / resume / stop
- Temperature control (nozzle + bed)
- Camera snapshot (MJPEG port 8080)

INSTALL:
Copy custom_components/elegoo_neptune4plus into /config/custom_components
Restart Home Assistant fully, then add integration "Elegoo Printer".

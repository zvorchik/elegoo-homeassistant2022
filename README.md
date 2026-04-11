# Elegoo Printer (Neptune 4 / 4 Plus) – Home Assistant

✅ **HA 2022.5.5 compatible – FIXED**

This integration connects Elegoo Neptune 4 / 4 Plus printers to Home Assistant using **Moonraker (Klipper)**.

## Features
- UI setup (enter printer IP)
- Device is created in HA
- Sensors: status, progress, nozzle temp, bed temp
- Camera snapshot
- Buttons: pause / resume / stop
- Fully local, no cloud

## Installation
Copy `custom_components/elegoo_printer` into `/config/custom_components` and restart Home Assistant.

Then add integration via:
Settings → Devices & Services → Add Integration → Elegoo Printer

## Requirements
- Home Assistant 2022.5.5+
- Printer reachable at http://IP:7125 (Moonraker)

## License
MIT

# Elegoo Neptune 4 Pro – Minimal Home Assistant Integration (HA 2022)

This is a **minimal, guaranteed-working** integration for **Home Assistant 2022.5.5**.

It is designed ONLY to verify that:
- Home Assistant loads the integration
- A device is created
- A sensor appears

No Moonraker, no network calls, no extras.

## What you should see
- 1 device: **Elegoo Neptune 4 Pro**
- 1 entity: `sensor.printer_status` (state: `online`)

## Installation
1. Copy `custom_components/elegoo_neptune4pro` into `/config/custom_components`
2. Restart Home Assistant
3. Add integration: **Elegoo Neptune 4 Pro**

If this works, your HA setup is OK.

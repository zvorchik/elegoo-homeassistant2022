# Elegoo Neptune 4 / 4 Plus – Home Assistant Integration

Native Home Assistant integration for Elegoo Neptune 4 and 4 Plus printers using **Moonraker (Klipper API)**.

## Features
- UI configuration (enter printer IP in UI)
- Local only (no cloud)
- Full printer telemetry
- Camera support
- Control buttons (pause / resume / stop)
- Compatible with Home Assistant 2022.5.5+

## Installation
1. Copy `custom_components/elegoo_neptune4plus` to `/config/custom_components`
2. Restart Home Assistant
3. Add integration via Settings → Devices & Services

## Entities
### Sensors
- Print status
- Progress (%)
- Nozzle temperature
- Bed temperature

### Camera
- Printer webcam snapshot

### Buttons
- Pause print
- Resume print
- Stop print

## Lovelace example
```yaml
type: picture-glance
camera_image: camera.elegoo_neptune4plus
entities:
  - sensor.print_status
  - sensor.progress
  - sensor.nozzle_temp
  - sensor.bed_temp
  - button.pause_print
  - button.resume_print
  - button.stop_print
```

## License
MIT


Elegoo Printer (Neptune 4 / 4 Plus) – HA 2022.5.5
=================================================

Moonraker-based integration adapted for Home Assistant **2022.5.5**.
Includes printer control, temperatures, camera, and **LED control via macros**.

Features:
- Printer device + sensors
- Pause / Resume / Cancel
- Hotend & Bed temperatures
- Camera snapshot (port 8080)
- LED control via macros:
  - FLASHLIGHT_SWITCH (Hotend LED)
  - MODLELIGHT_SWITCH (Logo LED)

Requirements:
- Moonraker accessible on http://PRINTER_IP:7125
- LED macros present in printer.cfg

Install:
Copy custom_components/elegoo_printer into /config/custom_components
Restart Home Assistant fully.
Add integration: Elegoo Printer.

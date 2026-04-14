
# Elegoo Neptune 4 Pro – Home Assistant (HA 2022.5.5)

Повна робоча інтеграція для керування принтером **Elegoo Neptune 4 Pro** через **Moonraker**.

## Можливості
- UI-додавання (вводиш IP принтера)
- Сенсори: статус, прогрес, температура сопла, температура стола
- Керування друком: Pause / Resume / Stop
- Зміна температур (nozzle / bed)
- Камера (snapshot з Moonraker)

## Вимоги
- Home Assistant 2022.5.5+
- Moonraker доступний на http://IP:7125

## Встановлення
1. Скопіюй `custom_components/elegoo_neptune4pro` у `/config/custom_components`
2. Повний reboot Home Assistant
3. Settings → Devices & Services → Add Integration → Elegoo Printer



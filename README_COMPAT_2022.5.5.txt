Это патч-набор для запуска `danielcherubini/elegoo-homeassistant` на Home Assistant Core 2022.5.5.

Что изменено:
- убрана платформа `image`, потому что Image entity появилась только в Home Assistant 2023.7;
- заменён вызов `async_forward_entry_setups(...)` на цикл `async_forward_entry_setup(...)`;
- добавлено хранение runtime-данных через `hass.data[DOMAIN][entry_id]` как запасной путь для старых ядер;
- обновлён `manifest.json`.

Как установить:
1. Скачай оригинальный репозиторий `danielcherubini/elegoo-homeassistant`.
2. Скопируй файлы из этого архива поверх оригинальных файлов в `custom_components/elegoo_printer/`.
3. Убедись, что в `custom_components/elegoo_printer/` не используется платформа `image`.
4. Перезапусти Home Assistant.

Важно:
- это best-effort backport без запуска реальных интеграционных тестов на HA 2022.5.5;
- если упрётся в ещё один новый API, следующим кандидатом будет правка `config_flow.py` или отдельных entity-платформ;
- превью/thumbnail как `image` entity в этой сборке отключены, но camera/sensor/button и остальная логика должны иметь больше шансов подняться на старом ядре.

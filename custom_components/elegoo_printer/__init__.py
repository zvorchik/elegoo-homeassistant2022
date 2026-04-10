"""
Minimal Elegoo Printer integration for Home Assistant Core 2022.5.5.
"""

from __future__ import annotations

import asyncio
from types import MappingProxyType
from typing import TYPE_CHECKING

from aiohttp import ClientError
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.loader import async_get_loaded_integration

from .api import ElegooPrinterApiClient
from .const import DOMAIN, LOGGER
from .coordinator import ElegooDataUpdateCoordinator
from .data import ElegooPrinterData
from .websocket.server import ElegooPrinterServer

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from .data import ElegooPrinterConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CAMERA,
    Platform.BUTTON,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ElegooPrinterConfigEntry,
) -> bool:
    """Set up Elegoo printer from a config entry."""
    coordinator = ElegooDataUpdateCoordinator(hass=hass, entry=entry)

    config = {
        **(entry.data or {}),
        **(entry.options or {}),
    }

    client = await ElegooPrinterApiClient.async_create(
        config=MappingProxyType(config),
        logger=LOGGER,
        hass=hass,
        config_entry=entry,
    )
    if client is None:
        raise ConfigEntryNotReady("Failed to connect to the printer")

    runtime_data = ElegooPrinterData(
        api=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    try:
        entry.runtime_data = runtime_data
    except AttributeError:
        pass

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = runtime_data

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        try:
            await client.elegoo_disconnect()
            await client.elegoo_stop_mqtt_broker()
            if client.server:
                await ElegooPrinterServer.release_reference()
        except Exception as cleanup_error:  # noqa: BLE001
            LOGGER.warning("Cleanup after failed setup: %s", cleanup_error)
        raise

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ElegooPrinterConfigEntry,
) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    runtime_data = getattr(entry, "runtime_data", None) or hass.data.get(
        DOMAIN, {}
    ).get(entry.entry_id)

    if unload_ok and runtime_data and (client := runtime_data.api):
        try:
            await asyncio.shield(client.elegoo_disconnect())
        except (asyncio.CancelledError, ClientError, OSError, RuntimeError) as err:
            LOGGER.warning("Error disconnecting client: %s", err, exc_info=True)

        try:
            should_stop = await asyncio.shield(
                ElegooPrinterServer.remove_printer_from_server(client.printer, LOGGER)
            )
            if not should_stop:
                await asyncio.shield(ElegooPrinterServer.release_reference())
        except (asyncio.CancelledError, OSError, RuntimeError) as err:
            LOGGER.warning(
                "Error removing printer from proxy server: %s", err, exc_info=True
            )

        try:
            await client.elegoo_stop_mqtt_broker()
        except (OSError, RuntimeError) as err:
            LOGGER.warning("Error stopping MQTT broker: %s", err, exc_info=True)

    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ElegooPrinterConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

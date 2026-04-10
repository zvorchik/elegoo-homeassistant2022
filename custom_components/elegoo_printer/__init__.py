"""
Custom integration to integrate elegoo_printer with Home Assistant.

For more details about this integration, please refer to
https://github.com/danielcherubini/elegoo-homeassistant
"""

from __future__ import annotations

import asyncio
from types import MappingProxyType
from typing import TYPE_CHECKING

from aiohttp import ClientError
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONF_IP_ADDRESS, Platform, UnitOfTime
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_registry import EntityRegistry, async_get
from homeassistant.loader import async_get_loaded_integration

from custom_components.elegoo_printer.websocket.client import ElegooPrinterClient

from .api import ElegooPrinterApiClient
from .const import (
    CONF_PROXY_ENABLED,
    CONFIG_VERSION_1,
    CONFIG_VERSION_2,
    CONFIG_VERSION_3,
    DOMAIN,
    LOGGER,
)
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
    Platform.LIGHT,
    Platform.BUTTON,
    Platform.FAN,
    Platform.SELECT,
    Platform.NUMBER,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ElegooPrinterConfigEntry,
) -> bool:
    """Set up the Elegoo printer integration from a configuration entry."""
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

    data = ElegooPrinterData(
        api=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    try:
        entry.runtime_data = data
    except AttributeError:
        pass

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = data

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        try:
            await client.elegoo_disconnect()
            await client.elegoo_stop_mqtt_broker()
            if client.server:
                await ElegooPrinterServer.release_reference()
        except Exception as cleanup_error:  # noqa: BLE001
            LOGGER.warning("Error during cleanup after failed setup: %s", cleanup_error)
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
    """Handle removal of an entry."""
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


async def async_migrate_entry(
    hass: HomeAssistant, config_entry: ElegooPrinterConfigEntry
) -> bool:
    """Migrate old entry."""
    if config_entry.version == CONFIG_VERSION_1:
        try:
            config = {
                **(config_entry.data or {}),
                **(config_entry.options or {}),
            }
            ip_address = config.get(CONF_IP_ADDRESS)
            proxy_enabled = config.get(CONF_PROXY_ENABLED, False)
            if ip_address is None:
                LOGGER.error("Config migration failed, IP address is null")
                return False

            LOGGER.debug(
                "Migrating from version %s with ip_address: %s and proxy: %s",
                config_entry.version,
                ip_address,
                proxy_enabled,
            )
            client = ElegooPrinterClient(
                ip_address=ip_address,
                logger=LOGGER,
                session=async_get_clientsession(hass),
            )
            printer = await hass.async_add_executor_job(
                client.discover_printer, ip_address
            )
            if printer and len(printer) > 0:
                printer[0].proxy_enabled = proxy_enabled
                new_data = printer[0].to_dict()

                hass.config_entries.async_update_entry(
                    config_entry, data=new_data, version=2
                )
                LOGGER.debug("Migration to version 2 successful")
            else:
                LOGGER.error("Config migration failed, no printer found")
                return False
        except (ConnectionError, IndexError, KeyError) as err:
            LOGGER.error("Error migrating config entry: %s", err)
            return False

    if config_entry.version == CONFIG_VERSION_2:
        entity_registry: EntityRegistry = async_get(hass)
        entries = entity_registry.entities.get_entries_for_config_entry_id(
            config_entry.entry_id
        )
        for entity_entry in entries:
            if (
                entity_entry.device_class == SensorDeviceClass.DURATION
                and entity_entry.native_unit_of_measurement == UnitOfTime.SECONDS
            ):
                entity_registry.async_update_entity(
                    entity_entry.entity_id,
                    native_unit_of_measurement=UnitOfTime.MILLISECONDS,
                )
        hass.config_entries.async_update_entry(config_entry, version=3)
        LOGGER.debug("Migration to version 3 successful")

    if config_entry.version == CONFIG_VERSION_3:
        LOGGER.debug("Migrating to version 4: updating unique IDs from 'name' to 'id'.")
        try:
            config = {
                **(config_entry.data or {}),
                **(config_entry.options or {}),
            }
            old_identifier_name = config.get("name")
            new_identifier = config.get("id")

            if not old_identifier_name or not new_identifier:
                LOGGER.error(
                    "Migration v3->v4 failed: 'name' or 'id' field is missing."
                )
                return False

            old_identifier_slug = old_identifier_name.lower().replace(" ", "_")
            LOGGER.debug(
                "MIGRATION CHECK: Using old identifier prefix: '%s'",
                old_identifier_slug,
            )

            if old_identifier_slug == new_identifier:
                LOGGER.debug("Identifier is already up-to-date. Finalizing migration.")
                hass.config_entries.async_update_entry(config_entry, version=4)
                return True

            device_registry = dr.async_get(hass)
            entity_registry = er.async_get(hass)

            device_entries = dr.async_entries_for_config_entry(
                device_registry, config_entry.entry_id
            )
            device_entry = device_entries[0] if device_entries else None
            if device_entry:
                new_identifiers = {(DOMAIN, new_identifier)}
                LOGGER.debug("Updating device identifiers to %s", new_identifiers)
                device_registry.async_update_device(
                    device_entry.id, new_identifiers=new_identifiers
                )

            entity_entries = er.async_get(
                hass
            ).entities.get_entries_for_config_entry_id(config_entry.entry_id)
            for entity_entry in entity_entries:
                LOGGER.debug(
                    "MIGRATION CHECK: Comparing with entity unique_id: '%s'",
                    entity_entry.unique_id,
                )
                if entity_entry.domain == "camera":
                    LOGGER.debug(
                        "Removing old camera entity '%s' to allow for clean re-creation.",
                        entity_entry.entity_id,
                    )
                    entity_registry.async_remove(entity_entry.entity_id)
                    continue

                if entity_entry.unique_id.lower().startswith(old_identifier_slug.lower()):
                    new_unique_id = entity_entry.unique_id.replace(
                        old_identifier_slug, new_identifier, 1
                    )
                    LOGGER.debug(
                        "Migrating entity '%s' to new unique_id: %s",
                        entity_entry.entity_id,
                        new_unique_id,
                    )
                    entity_registry.async_update_entity(
                        entity_entry.entity_id, new_unique_id=new_unique_id
                    )

            hass.config_entries.async_update_entry(config_entry, version=4)
            LOGGER.info(
                "Migration to version 4 successful for printer ID %s", new_identifier
            )

        except (KeyError, ValueError) as err:
            LOGGER.error(
                "Error migrating config entry to version 4: %s", err, exc_info=True
            )
            return False
    return True

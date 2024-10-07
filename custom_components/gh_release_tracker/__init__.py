import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.debug("Setting up gh_release_tracker integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up entry: %s", entry.data)
    
    # Store the config entry
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward entry setup to the sensor platform
    try:
        _LOGGER.debug("Forwarding entry setup to sensor platform for entry: %s", entry.entry_id)
        await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    except Exception as e:
        _LOGGER.error("Error during async_forward_entry_setups: %s", e)
        raise

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading entry: %s", entry.entry_id)
    
    # Unload the sensor platform
    try:
        await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    except Exception as e:
        _LOGGER.error("Error during async_forward_entry_unload: %s", e)
        return False
    
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

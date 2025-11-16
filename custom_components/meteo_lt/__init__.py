"""Meteo LT integration"""
from homeassistant.core import HomeAssistant

DOMAIN = "meteo_lt"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Meteo LT integration from YAML (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Meteo LT from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    return True

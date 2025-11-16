from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .api import MeteoLTApi

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    api = MeteoLTApi(session, entry.data["place"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(entry, ["weather"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "weather")
    return True

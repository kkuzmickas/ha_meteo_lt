import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, LOCATIONS_URL, CONF_LOCATION_ID, CONF_LOCATION_NAME

class MeteoLtConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Save the selected location
            location_name = user_input["location_id_name"]
            return self.async_create_entry(
                title=location_name,
                data={
                    CONF_LOCATION_ID: user_input["location_id"],
                    CONF_LOCATION_NAME: location_name
                }
            )

        # Fetch available locations
        locations = await self._fetch_locations()
        if not locations:
            errors["base"] = "cannot_connect"
            options = {}
        else:
            options = {loc["id"]: loc["name"] for loc in locations}

        schema = vol.Schema({
            vol.Required("location_id"): vol.In(options)
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def _fetch_locations(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(LOCATIONS_URL, timeout=10) as resp:
                    if resp.status != 200:
                        return None
                    return await resp.json()
        except Exception:
            return None

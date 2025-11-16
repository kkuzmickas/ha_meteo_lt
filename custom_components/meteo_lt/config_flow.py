import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
from .api import MeteoLTApi


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
async def async_step_user(self, user_input=None):
session = async_get_clientsession(self.hass)
api = MeteoLTApi(session, "vilnius")
places = await api.get_places()


choices = {p["code"]: f"{p['name']} ({p['administrativeDivision']})" for p in places}


schema = vol.Schema({vol.Required("place"): vol.In(choices)})


if user_input is not None:
return self.async_create_entry(
title=f"Meteo.lt ({choices[user_input['place']]})",
data={"place": user_input["place"]},
)


return self.async_show_form(step_id="user", data_schema=schema)

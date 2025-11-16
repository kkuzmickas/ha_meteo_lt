from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SENSOR_TYPES = {
    "temperature": "Current Temperature",
    "condition": "Weather Condition",
    "wind_speed": "Wind Speed",
    "humidity": "Humidity"
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [MeteoLtSensor(coordinator, key, name) for key, name in SENSOR_TYPES.items()]
    async_add_entities(sensors)

class MeteoLtSensor(SensorEntity):
    def __init__(self, coordinator, sensor_type, name):
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._name = name
        self._attr_unique_id = f"{coordinator.location_id}_{sensor_type}"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.coordinator.data
        if not data or "forecastTimestamps" not in data:
            return None
        current = data["forecastTimestamps"][0]
        return current.get(self.sensor_type)

    async def async_update(self):
        await self.coordinator.async_request_refresh()

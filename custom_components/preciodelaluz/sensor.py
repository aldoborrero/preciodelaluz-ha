from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import voluptuous as vol

from .api import PrecioDeLaLuzAPI

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "PrecioDeLaLuz"
CONF_CONVERT_UNITS = "convert_units"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_CONVERT_UNITS, default=False): cv.boolean,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    convert_units = config.get(CONF_CONVERT_UNITS)
    api = PrecioDeLaLuzAPI(convert_units=convert_units)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=api.get_all_prices,
        update_interval=None,
    )

    sensors = [
        PrecioDelaluzSensor(coordinator, api, name, "All Prices", "all"),
        PrecioDelaluzSensor(coordinator, api, name, "Average Price", "avg"),
        PrecioDelaluzSensor(coordinator, api, name, "Max Price", "max"),
        PrecioDelaluzSensor(coordinator, api, name, "Min Price", "min"),
        PrecioDelaluzSensor(coordinator, api, name, "Current Price", "now"),
        PrecioDelaluzSensor(coordinator, api, name, "Cheapest Prices", "cheapest"),
    ]

    async_add_entities(sensors, False)

    # Function to refresh data
    async def async_refresh_data(now=None):
        await coordinator.async_refresh()

    # Update data immediately
    await async_refresh_data()

    # Schedule updates every 24 hours
    async_track_time_interval(hass, async_refresh_data, timedelta(hours=24))


class PrecioDelaluzSensor(Entity):
    def __init__(self, coordinator, api, name, type, key):
        self.coordinator = coordinator
        self._api = api
        self._name = f"{name} {type}"
        self._type = type
        self._key = key
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        if not self.coordinator.data:
            return

        if self._type in ["Max Price", "Min Price"]:
            if not self._state:
                self._state = self.coordinator.data.get(self._key)
        elif self._type == "Current Price":
            current_hour = datetime.now().hour
            self._state = self.coordinator.data["all"].get(current_hour)
        else:
            self._state = self.coordinator.data.get(self._key)

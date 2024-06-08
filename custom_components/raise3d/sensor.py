"""Setup Sensor platform for Raise3D."""
import logging
from typing import Optional, Any

from homeassistant.const import (
    CONF_NAME,
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfMass,
    UnitOfTime,
)

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

from .const import (
    DOMAIN,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    PRINTER_SYSTEM_INFORMATION,
    CAMERA_INFORMATION,
    PRINTER_RUNNING_STATUS,
    PRINTER_BASIC_INFORMATION,
    PRINTER_NOZZLE_INFORMATION,
    PRINTER_CURRENT_JOB_INFORMATION
)

from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Do the setup entry."""
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]

    _LOGGER.debug("Setup entry %s %s", hub_name, hub)

    device_info = {
        "identifiers": {(DOMAIN, hub_name)},
        "name": hub_name,
        "manufacturer": ATTR_MANUFACTURER,
        "model": ATTR_MODEL,
    }

    entities = []

    for name, key, unit, icon in PRINTER_SYSTEM_INFORMATION.values():
        sensor = Raise3dSensor(
            hub_name, hub, device_info, "data", name, key, unit, icon
        )
        entities.append(sensor)

    for name, key, unit, icon in CAMERA_INFORMATION.values():
        camera = Raise3dSensor(
            hub_name, hub, device_info, "data", name, key, unit, icon
        )
        entities.append(camera)

    for name, key, unit, icon in PRINTER_RUNNING_STATUS.values():
        status = Raise3dSensor(
            hub_name, hub, device_info, "data", name, key, unit, icon
        )
        entities.append(status)

    for name, key, unit, icon in PRINTER_BASIC_INFORMATION.values():
        basic_info = Raise3dSensor(
            hub_name, hub, device_info, "data", name, key, unit, icon
        )
        entities.append(basic_info)

    for name, key, unit, icon in PRINTER_NOZZLE_INFORMATION.values():
        sensor = Raise3dSensor(
            hub_name, hub, device_info, "data", name, key, unit, icon
        )
        entities.append(sensor)

    for name, key, unit, icon in PRINTER_CURRENT_JOB_INFORMATION.values():
        sensor = Raise3dSensor(
            hub_name, hub, device_info, "data", name, key, unit, icon
        )
        entities.append(sensor)

    _LOGGER.debug("Entities added : %i", len(entities))

    async_add_entities(entities)

    return True


class Raise3dSensor(SensorEntity):
    """Raise3D Sensor class."""

    def __init__(
        self,
        platform_name,
        hub,
        device_info,
        prefix,
        name,
        key,
        unit,
        icon,
    ) -> None:
        """Initialize the sensor."""
        self._platform_name = platform_name
        self._hub = hub
        self._prefix = prefix
        self._key = key
        self._name = f"{self._platform_name} {name}"
        self._attr_unique_id = (
            f"{self._platform_name.lower()}_{self._prefix}_{self._key}"
        )
        self._unit_of_measurement = unit
        self._icon = icon
        self._device_info = device_info
        self._state = None
        if self._unit_of_measurement == UnitOfPower.KILO_WATT:
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_device_class = SensorDeviceClass.POWER
        if self._unit_of_measurement == UnitOfPower.WATT:
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_device_class = SensorDeviceClass.POWER
        if self._unit_of_measurement == UnitOfEnergy.WATT_HOUR:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            self._attr_device_class = SensorDeviceClass.ENERGY
        if self._unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            self._attr_device_class = SensorDeviceClass.ENERGY
        if self._unit_of_measurement == UnitOfTemperature.CELSIUS:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if self._unit_of_measurement == UnitOfMass.KILOGRAMS:
            self._attr_device_class = SensorDeviceClass.WEIGHT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if self.unit_of_measurement == PERCENTAGE:
            self._attr_device_class = SensorDeviceClass.POWER_FACTOR
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if self.unit_of_measurement == UnitOfTime.HOURS:
            self._attr_device_class = SensorDeviceClass.DURATION
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        if self.unit_of_measurement == UnitOfTime.MINUTES:
            self._attr_device_class = SensorDeviceClass.DURATION
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if self.unit_of_measurement == UnitOfTime.SECONDS:
            self._attr_device_class = SensorDeviceClass.DURATION
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if self.unit_of_measurement == UnitOfTime.MILLISECONDS:
            self._attr_device_class = SensorDeviceClass.DURATION
            self._attr_state_class = SensorStateClass.MEASUREMENT

        _LOGGER.debug(
            "Adding a Raise3D Sensor : %s, %s, %s, %s, %s, %s, %s, %s, %s",
            str(self._platform_name),
            str(self._hub),
            str(self._prefix),
            str(self._key),
            str(self._name),
            str(self._attr_unique_id),
            str(self._unit_of_measurement),
            str(self._icon),
            str(self._device_info),
        )

    async def async_added_to_hass(self):
        """Register callbacks."""
        #_LOGGER.debug("add to hass_pre")
        self._hub.async_add_raise3d_sensor(self._api_data_updated)
        #_LOGGER.debug("add to hass_post")

    async def async_will_remove_from_hass(self) -> None:
        """Register callbacks."""
        #_LOGGER.debug("remove from hass_pre")
        self._hub.async_remove_raise3d_sensor(self._api_data_updated)
        #_LOGGER.debug("remove from hass_pre")

    @callback
    def _api_data_updated(self):
        self.async_write_ha_state()

    @callback
    def _update_state(self):
        current_value = None

        current_value = self._hub.data[self._prefix][self._key]["val"]
        self._state = current_value

    @property
    def name(self):
        """Return the name."""
        return f"{self._name}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the sensor icon."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        current_value = None
        # current_value = self._hub.data[self._prefix][self._key]
        if not self._hub.data is None:  # noqa: E714
            try:
                current_value = self._hub.data[self._prefix][self._key]
            except Exception as e:
                # something wen wrong
                _LOGGER.debug("Exception: %s", repr(e.args))

        return current_value

    @property
    def extra_state_attributes(self):
        """Extra attribute."""
        return None

    @property
    def should_poll(self) -> bool:
        """Data is delivered by the hub."""
        return False

    @property
    def device_info(self) -> Optional[dict[str, Any]]:  # noqa: UP007
        """Device info."""
        return self._device_info

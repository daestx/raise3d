"""Constants for Raise3D printer configuration."""
from logging import Logger, getLogger

from homeassistant.const import (
    UnitOfTime,
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfMass,
    UnitOfPower,
    UnitOfEnergy,
)


LOGGER: Logger = getLogger(__package__)

NAME = "Raise3D"
DOMAIN = "raise3d"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

DEFAULT_NAME = "Raise3D"
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_PORT = 10800
DEFAULT_IP = "aaa.bbb.ccc.ddd"

CONF_NAME = "Raise3D"
CONF_SCAN_INTERVAL = 10
CONF_PORT = 10800
CONF_IP = "IP"

ATTR_STATUS_DESCRIPTION = "status_description"
ATTR_MANUFACTURER = "Raise 3D"
ATTR_MODEL = "Pro2"

SYSTEM_SENSOR_TYPES = {
    "L_status": [
        "Outside Temperature",
        "L_status",
        UnitOfTemperature.CELSIUS,
        None,
    ],
    "L_errors": [
        "System Errors",
        "L_errors",
        None,
        "mdi:alert-circle",
    ],
}


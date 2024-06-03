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
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_PORT = 10800
DEFAULT_IP = "192.168.110.35"
DEFAULT_PASSWORD = "password"

# titles in configuration flows are define in strings and translation json files
CONF_PORT = "conf_port"
CONF_PASSWORD = "conf_password"

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


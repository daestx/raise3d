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
DEFAULT_IP = "192.168.110.25"
DEFAULT_PASSWORD = "password"

# titles in configuration flows are define in strings and translation json files
CONF_PORT = "conf_port"
CONF_PASSWORD = "conf_password"

ATTR_MANUFACTURER = "Raise 3D"
ATTR_MODEL = "Pro2"


#Printer System Information
PRINTER_SYSTEM_INFORMATION = {
    "L_serial_number": [
        "Serial number",
        "L_serial_number",
        None,
        None,
    ],
    "L_api_version": [
        "API version",
        "L_api_version",
        None,
        "mdi:alert-circle",
    ]
}


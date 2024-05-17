"""Constants for Raise3D printer configuration"""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Raise3D"
DOMAIN = "raise3d"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

DEFAULT_NAME = "Raise3D"
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_PORT = 10800
DEFAULT_IP = "aaa.bbb.ccc.ddd"

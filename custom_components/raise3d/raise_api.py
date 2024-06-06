"""Add API interface for Raise3D printers."""

import hashlib
import time
import json
import urllib3
import logging

_LOGGER = logging.getLogger(__name__)


class raise3d:
    """Class for API functions."""
    def requestHttp(self, url):
        http = urllib3.PoolManager()
        try:
            response = http.request('GET', url)
            data = response.data
            values = json.loads(data)
            return values
        except:
            return {'status': 0}

    def calc_hash(self, plain):
        """Hash value generation."""
        hash = hashlib.sha1(plain.encode('utf-8')).hexdigest()
        _LOGGER.debug("sha1:%s", hash)
        hash = hashlib.md5(hash.encode('utf-8')).hexdigest()
        _LOGGER.debug("md5:%s", hash)
        return hash

    def getTime(self):
        """Return ms epoch timestamp."""
        millis_since_epoch = time.time_ns() // 1000000
        return str(millis_since_epoch)

    def getLogin(self, url, port, password):
        """Receive API token from printer."""
        time = self.getTime()
        plain = "password=" + password + "&timestamp=" + time
        _LOGGER.debug("plain:%s", plain)
        hash = self.calc_hash(plain)

        # generate url string with URL parameter for hash value and timestamp according API doc
        _url = url + ":" + port + "/v1/login?sign=" + hash + "&timestamp=" + time
        _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            token = json["data"]["token"]
            _LOGGER.debug("Token:%s", token)
            return token

        # in case of error or timeout
        return None

    def getInfo(self, url, port, token):
        """Get printer system information, like language, brightness."""
        _url = url + ":" + port + "/v1/printer/system?token=" + token
        _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            return json

        # in case of error or timeout
        return None

    def getPrinterStatus(self, url, port, token):
        """Get printer running status."""
        _url = url + ":" + port + "/v1/printer/runningstatus?token=" + token
        _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            return json

        # in case of error or timeout
        return None

    def getCurrentJob(self,  url, port, token):
        """Get current job information."""
        _url = ip + ":" + port + "/v1/job/currentjob?token=" + token
        _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            return json

        # in case of error or timeout
        return None

"""Add API interface for Raise3D printers."""

import hashlib
import time
import json
import urllib3
import logging
import requests

_LOGGER = logging.getLogger(__name__)


class raise3d:
    """Class for API functions."""

    def requestHttp(self, url):
        """Receive data by accessing the printer URL."""
        retry = urllib3.Retry(
            total=3,
            raise_on_status=True,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        timeout = urllib3.Timeout(1.0)

        http = urllib3.PoolManager(
            retries=retry,
            timeout=timeout
        )

        # disable urllib3 Retrying warning messages to not clutter log files
        logging.getLogger(
            requests.packages.urllib3.__package__).setLevel(logging.ERROR)

        try:
            response = http.request('GET', url)
            data = response.data
            values = json.loads(data)
            return values
        except Exception as e:  # noqa: F841
            # _LOGGER.debug("Exception: %s", repr(e.args))
            return {'status': 0}

    def calc_hash(self, plain):
        """Hash value generation."""
        hash = hashlib.sha1(plain.encode('utf-8')).hexdigest()
        # _LOGGER.debug("sha1:%s", hash)
        hash = hashlib.md5(hash.encode('utf-8')).hexdigest()
        # _LOGGER.debug("md5:%s", hash)
        return hash

    def getTime(self):
        """Return ms epoch timestamp."""
        millis_since_epoch = time.time_ns() // 1000000
        return str(millis_since_epoch)

    def getLogin(self, url, port, password):
        """Receive API token from printer."""
        time = self.getTime()
        plain = "password=" + password + "&timestamp=" + time
        # _LOGGER.debug("plain:%s", plain)
        hash = self.calc_hash(plain)

        # generate url string with URL parameter for hash value and timestamp according API doc
        _url = url + ":" + port + "/v1/login?sign=" + hash + "&timestamp=" + time
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            # remove status key from json object since it is not needed anymore
            # and leads to issues when iterating
            del json['status']
            token = json["data"]["token"]
            # _LOGGER.debug("Token:%s", token)
            return token

        # in case of error or timeout
        return None

    def getInfo(self, url, port, token):
        """Get printer system information, like language, brightness."""
        _url = url + ":" + port + "/v1/printer/system?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getCameraInformation(self,  url, port, token):
        """Get camera information."""
        _url = url + ":" + port + "/v1/printer/camera?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getPrinterRunningStatus(self, url, port, token):
        """Get printer running status."""
        _url = url + ":" + port + "/v1/printer/runningstatus?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getPrinterBasicInformation(self,  url, port, token):
        """Get Printer Basic Information."""
        _url = url + ":" + port + "/v1/printer/basic?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getLeftNozzleInformation(self,  url, port, token):
        """Get Left Nozzle Information."""
        _url = url + ":" + port + "/v1/printer/nozzle1?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            temp = []
            # key are the same for left and right nozzler. Need to change this
            for item in json['data']:
                temp.append(item)
            for item in temp:
                json['data']['LN_' + item] = json['data'].pop(item)

            return json

        # in case of error or timeout
        return None

    def getRightNozzleInformation(self,  url, port, token):
        """Get Right Nozzle Information."""
        _url = url + ":" + port + "/v1/printer/nozzle2?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            temp = []
            # key are the same for left and right nozzler. Need to change this
            for item in json['data']:
                temp.append(item)
            for item in temp:
                json['data']['RN_' + item] = json['data'].pop(item)

            return json

        # in case of error or timeout
        return None

    def SetLeftNozzleTemperature(self,  url, port, token, temp):
        """Set Left Nozzle Temperatur."""
        _url = url + ":" + port + "/v1/printer/nozzle1/temp/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def SetRightNozzleTemp(self,  url, port, token, temp):
        """Set Right Nozzle Temperature."""
        _url = url + ":" + port + "/v1/printer/nozzle2/temp/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def SetLeftNozzleFlowRate(self,  url, port, token, flow):
        """Set Left Nozzle Flow Rate."""
        _url = url + ":" + port + "/v1/printer/nozzle1/flowrate/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def SetRightNozzleFlowRate(self,  url, port, token, flow):
        """Set Right Nozzle Flow Rate."""
        _url = url + ":" + port + "/v1/printer/nozzle2/flowrate/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def SetHeatBedTemperature(self,  url, port, token, flow):
        """Set Heat Bed Temperature."""
        _url = url + ":" + port + "/v1/printer/heatbedtemp/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def SetFeedRate(self,  url, port, token, feed):
        """Set Feed Rate."""
        _url = url + ":" + port + "/v1/printer/feedrate/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def SetFanSpeed(self,  url, port, token, fan):
        """Set Feed Rate."""
        _url = url + ":" + port + "/v1/printer/feedrate/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        # modify post access
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def setAxisShiftControl(self,  url, port, token, axis):
        """Set Axis Shift Control."""
        _url = url + ":" + port + "/v1/job/currentjob?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getCurrentJob(self,  url, port, token):
        """Get current job information."""
        _url = url + ":" + port + "/v1/job/currentjob?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

    def setCurrentJob(self,  url, port, token, job):
        """Set current job operation."""
        _url = url + ":" + port + "/v1/job/currentjob/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def setCreateNewJob(self,  url, port, token, job):
        """Create New Job."""
        _url = url + ":" + port + "/v1/job/newjob/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def setRecoverLastJob(self,  url, port, token, job):
        """Recover Last Job."""
        _url = url + ":" + port + "/v1/job/recover/set?token=" + token
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getFileList(self,  url, port, token, job):
        """Get File List."""
        _url = url + ":" + port + "/v1/job/fileops/list?token=" + \
            token + "&dir=Local/webapi_store&start_pos=0&max_num=100"
        # _LOGGER.debug("URL:%s", _url)
        json = self.requestHttp(_url)
        # _LOGGER.debug("Json:%s", json)

        if json["status"] == 1:
            del json['status']
            return json

        # in case of error or timeout
        return None

    def getSimulatedData(self):
        """Get simulated data."""
        with open('doc/api_data.json') as myfile:
            data = json.load(myfile)

        return data

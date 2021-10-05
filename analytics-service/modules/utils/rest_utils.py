from os import getenv
import requests

class RestApi:
    def __init__(self, base_url):
        self.url = base_url

    def __get(self, query: str, params = None):
        resp = requests.get(self.url + query, params=params)
        resp.raise_for_status()
        return resp

    def get_json(self, path: str, params=None):
        return self.__get(path, params).json()


class AlertApi(RestApi):
    def __init__(self):
        super().__init__(getenv("ALERT_SERVICE_URL"))
        # super().__init__("http://localhost:3000")

    def get_packets(self):
        return self.get_json(f"/etl/packets")
    
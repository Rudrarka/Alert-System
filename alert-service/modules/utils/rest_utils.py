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


class MockerApi(RestApi):
    def __init__(self):
        super().__init__(getenv("MOCKER_URL"))

    def search_products(self, keyword):
        query = f"_sort=price&_order=asc&q={keyword}&_limit=20"
        return self.get_json(f"/products",query)
    
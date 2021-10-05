from os import getenv
import requests

class RestApi:
    def __init__(self, base_url: str):
        self.url = base_url

    def post_json(self, path, json):
        resp = requests.post(self.url + path, json=json)
        resp.raise_for_status()
        return resp.json()

    def put_json(self, path, json):
        resp = requests.put(self.url + path, json=json)
        resp.raise_for_status()
        return resp.json()
    
    def delete_json(self, path, json):
        resp = requests.delete(self.url + path, json=json)
        resp.raise_for_status()
        return resp.json()

class Mockerpi(RestApi):
    def __init__(self):
        super().__init__(getenv("MOCKER_URL"))

    def update_product(self, product):
        path = f"/{product['id']}"
        self.put_json('/products', path=path, json=product)



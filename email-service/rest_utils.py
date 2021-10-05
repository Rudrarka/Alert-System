import os
import requests

class RestApi:
    def __init__(self, base_url: str, api_key: str):
        self.url = base_url
        self.headers = {'X-API-Key': api_key}

    def patch_json(self, path, json):
        resp = requests.patch(self.url + path, headers=self.headers, json=json)
        resp.raise_for_status()
        return resp.json()


class AlertApi(RestApi):
    def __init__(self):
        super().__init__(os.getenv('APP_URL'), os.getenv('API_KEY'))

    def acknowledge_mail_sent(self, id):
        params = {"email_sent": True}
        return self.patch_json(f"/{id}", params)
from requests import post, get
from json import dumps


class JsonRequestBase:

    host = 'http://127.0.0.1:5000'
    headers = {'Content-Type': 'application/json'}

    def get(self, url):
        response = get(url, headers=self.headers).json()
        return response

    def post(self, url, data):
        response = post(url, data=dumps(data), headers=self.headers).json()
        return response

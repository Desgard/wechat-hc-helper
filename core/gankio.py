import requests
import json


def fuli():
    resp = requests.get("http://gank.io/api/today")
    data = json.loads(s=resp.content)['results']["福利"]

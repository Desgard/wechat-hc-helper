from log import logger

import re
import requests
import json


def valid_bytedance_jd_query(msg):
    m = re.match(r'^.+?bd-search:(.+)$', msg.text)
    if m:
        query = m.group(1)
        logger.info('query - {q}'.format(q=query))
        return query
    return None


def resolve_pos(item: dict):
    return {
        "id": item['sub_name'],
        "name": item['name'],
        "base": item['city'],
        "summary": item['summary'],
        "description": item["description"],
    }


def query_bytedance_jd(query: str) -> dict:
    url = "https://job.bytedance.com/api/recruitment/position/list/"

    querystring = {"type": "3", "q1": query, "limit": "5", "offset": "0"}

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'content-type': 'application/json; charset=utf8',
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    res = json.loads(response.text)
    logger.info(res)
    return list(map(resolve_pos, res['positions']))

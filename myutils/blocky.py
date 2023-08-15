import time

import requests

BLOCKY_API = 'https://blocky.greatfire.org/api'


def test_now(url):
    headers = {
        'authority': 'blocky.greatfire.org',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://blocky.greatfire.org',
        'referer': 'https://blocky.greatfire.org/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
    }

    params = {
        'url': str(url),
        'timestamp': str(int(time.time())),
    }

    json_data = {}

    response = requests.post(BLOCKY_API + '/test_now',
                             params=params, headers=headers, json=json_data)

    response.raise_for_status()

    return response.text


if __name__ == '__main__':
    print(test_now('https://www.google.com'))

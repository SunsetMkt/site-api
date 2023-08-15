import json
import time

import requests

BLOCKY_API = 'https://blocky.greatfire.org/api'


def json_parser(text):
    try:
        return json.loads(text)
    except:
        # Remove the last line of text and try again
        lines = text.splitlines()
        text = '\n'.join(lines[:-1])
        try:
            return json.loads(text)
        except:
            return text


headers = {
    'authority': 'blocky.greatfire.org',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://blocky.greatfire.org',
    'referer': 'https://blocky.greatfire.org/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
}


def test_now(url):
    params = {
        'url': str(url),
        'timestamp': str(int(time.time())),
    }
    json_data = {}
    response = requests.post(BLOCKY_API + '/test_now',
                             params=params, headers=headers, json=json_data)
    response.raise_for_status()
    return json_parser(response.text)


def search(url):
    params = {
        'btnSearch': 'false',
        'url': str(url),
    }
    response = requests.get(BLOCKY_API+'/search/',
                            params=params, headers=headers)
    response.raise_for_status()
    return json_parser(response.text)


def get_result_of_url_id(id):
    json_data = {}
    timestamp = str(int(time.time()))
    response = requests.post(
        BLOCKY_API + f'/url_tests/{id}?{timestamp}', headers=headers, json=json_data)
    response.raise_for_status()
    return json_parser(response.text)


def get_detail_of_report_id(id):
    timestamp = str(int(time.time()))
    response = requests.get(
        BLOCKY_API + f'/url_test_result/{id}?{timestamp}', headers=headers)
    response.raise_for_status()
    return json_parser(response.text)


def get_latest_report_of_url(url):
    url_id = search(url)['d'][0]['id']
    report_id = get_result_of_url_id(url_id)['d'][0]['id']
    return get_detail_of_report_id(report_id)


if __name__ == '__main__':
    # print(test_now('https://www.google.com'))
    # print(search('https://www.google.com'))
    # print(get_result_of_url_id(2009))
    print(get_latest_report_of_url('https://www.google.com'))

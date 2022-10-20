import urllib

import flask
import pybase16384 as pybs
import requests


def decode(string):
    return pybs.decode_string(string)


def encode(string):
    return pybs.encode_string(string)


def get_gist_info(gist_id):
    url = 'https://api.github.com/gists/{}'.format(gist_id)
    headers = {
        "Accept": "application/vnd.github+json"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_first_gist(gist_id):
    gist_info = get_gist_info(gist_id)
    if gist_info:
        return gist_info['files'].values()[0]['content']
    else:
        return "# Error"


def render_gist(encoded):
    encoded = urllib.parse.unquote(encoded)
    gist_id = decode(encoded)
    gist = get_first_gist(gist_id)
    return flask.render_template_string(title=encoded, gist=gist)

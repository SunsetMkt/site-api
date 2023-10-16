import urllib

import flask
import pybase16384 as pybs
import requests


def decode(string):
    return pybs.decode_string(string)


def encode(string):
    return pybs.encode_string(string)


def get_gist_info(gist_id):
    """
    Get gist info from github api
    """
    url = "https://api.github.com/gists/{}".format(gist_id)
    headers = {"Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_first_gist(gist_id):
    """
    Get first gist from gist_id
    Actually the first one in dict, but who cares?
    """
    gist_info = get_gist_info(gist_id)
    if gist_info:
        files = gist_info["files"]
        for i in files:  # Who cares?
            return files[i]["content"]
    else:
        return "# Error"


def render_gist(encoded):
    encoded = urllib.parse.unquote(encoded)
    gist_id = decode(encoded)
    gist = get_first_gist(gist_id)
    return flask.render_template("gist.html", title=encoded, gist=gist)

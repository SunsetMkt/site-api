import urllib

import flask
import pybase16384 as pybs


def toB():
    # Get all args
    args = flask.request.args
    # If have no args
    if len(args) == 0:
        # 404
        return flask.abort(404)
    # Try to get arg "url"
    url = flask.request.args.get("url")
    # if url is empty, get request url
    if url == None:
        url = flask.request.url
        # decode url
        url = urllib.parse.unquote(url)
        # Remove host/api/url? from url
        url = url.replace(flask.request.host_url + "api/url?", "")
    return flask.Response(pybs.encode_string(url), mimetype="text/plain")


def fromB(url):
    # 302
    url = urllib.parse.unquote(url)
    return flask.Response(
        pybs.decode_string(url),
        status=302,
        headers={"Location": pybs.decode_string(url)},
    )

import re

import flask
import pybase16384 as pybs


def handle_url(url):
    # http://urlregex.com/
    regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    if re.match(regex, url):
        # return pybs.encode_string(url)
        return flask.Response(pybs.encode_string(url), mimetype='text/plain')
    else:
        # return pybs.decode_string(url)
        # 302
        return flask.Response(status=302, headers={"Location": pybs.decode_string(url)})

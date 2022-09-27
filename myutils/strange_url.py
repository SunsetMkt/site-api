import flask
import pybase16384 as pybs


def toB(url):
    return flask.Response(pybs.encode_string(url), mimetype='text/plain')


def fromB(url):
    # 302
    try:
        return flask.Response(pybs.decode_string(url), status=302, headers={'Location': pybs.decode_string(url)})
    except:
        raise Exception(url)

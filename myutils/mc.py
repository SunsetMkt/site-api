import base64
import json

import flask
import requests


def mcskin(id='notch', format='image'):
    # If id is empty, return help message
    if id == None:
        return "Usage: ?id=[Player ID]&format=[url/json/image]"
    # If format is empty, set format to "url"
    if format == None:
        format = "url"
    API_PROFILE_URL = "https://api.mojang.com/users/profiles/minecraft/"
    API_SESSION_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"
    # Get profile
    profile = requests.get(API_PROFILE_URL + id).json()
    sessionid = profile["id"]
    session = requests.get(API_SESSION_URL + sessionid).json()

    textureB64 = session["properties"][0]["value"]
    textureRaw = base64.b64decode(textureB64)
    textureJson = json.loads(textureRaw)

    skinUrl = textureJson["textures"]["SKIN"]["url"]

    if format == "url":
        return skinUrl
    elif format == "json":
        dict = {"url": skinUrl, 'profile': profile, 'session': session}
        return flask.Response(json.dumps(dict), mimetype='application/json')
    elif format == "image":
        # Get image
        image = requests.get(skinUrl).content
        return flask.Response(image, mimetype="image/png")
    else:
        return flask.Response(skinUrl, mimetype='text/plain')

import flask
import requests


def getGitHubAvatar(username, type="raw"):
    # Fetch avatar
    # If type is raw, return raw image
    if type == "raw":
        # Get avatar url
        avatar_url = requests.get("https://api.github.com/users/" + username).json()[
            "avatar_url"
        ]
        rawimage = requests.get(avatar_url).content
        # Return raw image
        return flask.Response(rawimage, mimetype="image/png")
    # If type is json
    if type == "json":
        # Return avatar url
        return flask.jsonify(
            requests.get("https://api.github.com/users/" + username).json()
        )
    # If type is redirect
    if type == "redirect":
        # Redirect to avatar url
        return flask.redirect(
            requests.get("https://api.github.com/users/" + username).json()[
                "avatar_url"
            ]
        )
    if type == "text":
        # Return avatar url
        return flask.Response(
            requests.get("https://api.github.com/users/" + username).json()[
                "avatar_url"
            ],
            mimetype="text/plain",
        )
    # If type is not raw, json, redirect, text, return text
    return flask.Response(
        requests.get("https://api.github.com/users/" + username).json()["avatar_url"],
        mimetype="text/plain",
    )

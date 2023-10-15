import base64
import json
import os
import random
import sys
import time
import traceback

import coolname
import flask
import flask_gzipbomb
import lorem
import pybase16384 as pybs
import requests

import myutils

# Get current flask app
app = flask.current_app
# blueprint
urls_blueprint = flask.Blueprint("v1", __name__)


# if path is empty, redirect to /api/v1
@urls_blueprint.route("/")
def api_v1_root():
    """
    Handle /api/v1
    Redirect to /api/v1
    ---
    tags:
        - redirect
    responses:
        301:
          description: Redirect to /api/v1"""
    return flask.redirect("/api/v1")


# if path is not empty, use different api
# for example, /api/v1/echo?text=hello
# will return {"text": "hello"}


@urls_blueprint.route("/echo")
def api_v1_echo():
    """
    Echo text
    Return json with text
    ---
    tags:
        - echo
    parameters:
        - name: text
          in: query
          type: string
          required: true
    responses:
        200:
            description: Echo text"""
    return flask.jsonify({"text": flask.request.args.get("text")})


# postecho will return the post data


@urls_blueprint.route("/postecho", methods=["POST"])
def api_v1_postecho():
    """
    Echo post data
    Return json with post data
    ---
    tags:
        - echo
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: postecho
          properties:
            text:
              type: string
              description: text to echo
    responses:
        200:
            description: Echo jsonified request body"""
    return flask.jsonify(flask.request.json)


# statuscode will return the given status code


@urls_blueprint.route("/statuscode")
def api_v1_statuscode():
    """
    Return status code
    Return status code
    ---
    tags:
        - debug
    parameters:
        - name: code
          in: query
          type: integer
          required: true
          description: Status code to return
    responses:
        200:
            description: Return status code"""
    return flask.Response(status=int(flask.request.args.get("code")))


# random will return a random number


@urls_blueprint.route("/random")
def api_v1_random():
    """
    Return random number
    Return random number
    ---
    tags:
        - debug
        - random
    responses:
        200:
            description: Random number"""
    return flask.jsonify({"random": random.random()})


# time return timestamp


@urls_blueprint.route("/time")
def api_v1_time():
    """
    Return timestamp
    Return timestamp
    ---
    tags:
        - debug
    responses:
        200:
            description: Timestamp"""
    return flask.jsonify({"time": time.time()})


# pi will calculate pi at the given digit


@urls_blueprint.route("/pi")
def api_v1_pi():
    """
    Calculate pi
    Calculate pi at the given digit
    ---
    tags:
        - pi
        - debug
    parameters:
        - name: n
          in: query
          type: integer
          required: true
          description: Number of digits to calculate pi to
    responses:
        200:
            description: Pi and calculate time"""
    n = flask.request.args.get("n")
    return flask.jsonify(myutils.pi.cal(str(n)))


# hello api
# return {"hello": "world"}


@urls_blueprint.route("/hello")
def api_v1_hello():
    """
    Return hello world
    return {"hello": "world"}
    ---
    tags:
        - debug
    responses:
        200:
            description: Hello world"""
    return flask.jsonify({"hello": "world"})


# status api
# return {"status": "ok"}


@urls_blueprint.route("/status")
def api_v1_status():
    """
    Return status
    return {"status": "ok"}
    ---
    tags:
        - debug
    responses:
        200:
            description: Status"""
    return flask.jsonify({"status": "ok"})


# env api
# return all flask config information, environment variables, Python config & sys info in json


@urls_blueprint.route("/env")
def api_v1_env():
    """
    Return environment information
    return all flask config information, environment variables, Python config & sys info in json
    ---
    tags:
        - debug
        - dangerous
    responses:
        200:
            description: Env"""
    # json_str = json.dumps({**os.environ, **app.config}, default=str)

    # get all flask config information
    flask_config = {}
    for key in app.config:
        flask_config[key] = app.config[key]

    # get all environment variables
    env = {}
    for key in os.environ:
        env[key] = os.environ[key]

    # get all Python config & sys info
    python_config = {}
    for key in dir(sys):
        python_config[key] = getattr(sys, key)

    outputJson = json.dumps(
        {"flask_config": flask_config, "env": env, "python_config": python_config},
        default=str,
    )

    return flask.Response(outputJson, mimetype="application/json")


# 33reply api
# Bilibili Reply Fetcher for 662016827293958168


@urls_blueprint.route("/33reply")
def api_v1_33reply():
    """
    Bilibili Reply Fetcher
    Bilibili Reply Fetcher for 662016827293958168
    ---
    tags:
        - bili
    parameters:
        - name: next
          in: query
          type: integer
          required: false
          description: Page number
          default: 0
        - name: oid
          in: query
          type: string
          required: false
          description: Bilibili oid
          default: '662016827293958168'
    responses:
        200:
            description: 33reply"""
    # Get request args: next, oid
    next = flask.request.args.get("next")
    oid = flask.request.args.get("oid")
    # If next is not set, set it to 0
    if next == None:
        next = 0
    # If oid is not set, set it to 662016827293958168
    if oid == None:
        oid = 662016827293958168
    return flask.jsonify(myutils.bili.threethreeReply(next, oid))


# getBiliUserInfo api
# Bilibili User Info Fetcher


@urls_blueprint.route("/getBiliUserInfo")
def api_v1_getBiliUserInfo():
    """
    Bilibili User Info Fetcher
    Bilibili User Info Fetcher
    ---
    tags:
        - bili
    parameters:
        - name: mid
          in: query
          type: string
          required: false
          description: Bilibili mid
          default: '22259558'
    responses:
        200:
            description: BiliUserInfo"""
    # Get request args: mid
    mid = flask.request.args.get("mid")
    # If mid is not set, set it to 22259558
    if mid == None:
        mid = 22259558
    return flask.jsonify(myutils.bili.getBiliUserInfo(mid))


# getGitHubAvatar api
# GitHub Avatar Fetcher


@urls_blueprint.route("/getGitHubAvatar")
def api_v1_getGitHubAvatar():
    """
    GitHub Avatar Fetcher
    GitHub Avatar Fetcher
    ---
    tags:
        - github
    parameters:
        - name: username
          in: query
          type: string
          required: false
          description: GitHub username
          default: octocat
        - name: type
          in: query
          type: string
          required: false
          description: Response type
          enum: [raw, json, redirect, text]
          default: raw
    responses:
        200:
            description: GitHubAvatar"""
    # Get args: username, type
    username = flask.request.args.get("username")
    type = flask.request.args.get("type")
    # If username is not set, set it to octocat
    if username == None:
        username = "octocat"
    # If type is not set, set it to raw
    if type == None:
        type = "raw"
    return myutils.github.getGitHubAvatar(username, type)


# ikialive api
# Bilibili user live status fetcher


@urls_blueprint.route("/ikialive")
def api_v1_ikialive():
    """
    Bilibili user live status fetcher
    Bilibili user live status fetcher
    ---
    tags:
        - bili
    parameters:
        - name: mid
          in: query
          type: string
          required: false
          description: Bilibili mid
          default: '22259558'
    responses:
        200:
            description: ikialive status"""
    # Get request args: mid
    mid = flask.request.args.get("mid")
    # If mid is not set, set it to 22259558
    if mid == None:
        mid = 22259558
    return flask.Response(myutils.bili.ikialive(mid), mimetype="text/plain")


# kizunaai api
# KizunaAI Directories List


@urls_blueprint.route("/kizunaai")
def api_v1_kizunaai():
    """
    KizunaAI Resource Path List
    KizunaAI Directories List
    ---
    tags:
        - kizunaai
    parameters:
        - name: id
          in: query
          type: integer
          required: true
          description: Must be 63045280
          default: 63045280
        - name: date
          in: query
          type: string
          required: true
          description: Date in format MM-DD
    responses:
        200:
            description: Resource URL or error code"""
    # Get args: id, date
    id = flask.request.args.get("id")
    date = flask.request.args.get("date")
    return flask.Response(myutils.kizunaai.kizunaai(id, date), mimetype="text/plain")


# mcskin api
# Get Minecraft skin from a Minecraft username


@urls_blueprint.route("/mcskin")
def api_v1_mcskin():
    """
    Get Minecraft skin from a Minecraft username
    Get Minecraft skin from a Minecraft username
    ---
    tags:
        - mc
    parameters:
        - name: id
          in: query
          type: string
          required: true
          description: Player Name
        - name: format
          in: query
          type: string
          required: false
          enum: [url, json, image]
          default: url
          description: Response type
    responses:
        200:
            description: Skin URL, player info json or skin image"""
    # Get args: id, format
    id = flask.request.args.get("id")
    format = flask.request.args.get("format")
    return myutils.mc.mcskin(id, format)


# bomb api
# return a gzip bomb


@urls_blueprint.route("/bomb")
def api_v1_bomb():
    """
    Return Gzip Bomb
    return a gzip bomb
    ---
    tags:
        - debug
        - dangerous
    responses:
        200:
            description: Bomb"""
    return flask_gzipbomb.GzipBombResponse(size="10G")


# ZeroDivisionError api
# Trigger a ZeroDivisionError on purpose


@urls_blueprint.route("/ZeroDivisionError")
def api_v1_ZeroDivisionError():
    """
    Return ZeroDivisionError
    Trigger a ZeroDivisionError on purpose
    ---
    tags:
        - debug
    responses:
        500:
            description: ZeroDivisionError"""
    return 1 / 0


# raiseException api
# Trigger a Exception on purpose


@urls_blueprint.route("/raiseException")
def api_v1_raiseException():
    """
    Trigger a Exception on purpose
    Trigger a Exception on purpose
    ---
    tags:
        - debug
    responses:
        500:
            description: Exception"""
    raise Exception("This is a test exception.")


# raiseHTTPError api
# Trigger a HTTPError on purpose


@urls_blueprint.route("/raiseHTTPError")
def api_v1_raiseHTTPError():
    """
    Trigger a HTTP Error on purpose
    Trigger a HTTP Error on purpose
    ---
    tags:
        - debug
    parameters:
        - name: status
          in: query
          type: integer
          required: true
          description: HTTP status code
    responses:
        500:
            description: HTTPError"""
    # Get status
    status = flask.request.args.get("status")
    # raise
    flask.abort(int(status))


# freenom api
# Call freenom.fnRenew(username, password)
# Check Freenom Domain Expiration Info


@urls_blueprint.route("/freenom", methods=["GET"])
def api_v1_freenom():
    """
    Check Freenom Domain Expiration Info
    Check Freenom Domain Expiration Info
    ---
    tags:
        - freenom
    parameters:
        - name: username
          in: query
          type: string
          required: true
          description: Freenom username
        - name: password
          in: query
          type: string
          required: true
          description: Freenom password
    responses:
        200:
            description: Freenom domain expiration info"""
    # Get args: username, password
    username = flask.request.args.get("username")
    password = flask.request.args.get("password")
    # If username or password is empty, return help message
    if username == None or password == None:
        return flask.Response(
            'Usage: \nGET ?username=[username]&password=[password]\nPOST {"username": "[username]", "password": "[password]"}',
            mimetype="text/plain",
            status=400,
        )
    return flask.Response(
        myutils.freenom.fnRenew(username, password), mimetype="text/plain"
    )


@urls_blueprint.route("/freenompost", methods=["POST"])
def api_v1_freenompost():
    """
    Check Freenom Domain Expiration Info
    Check Freenom Domain Expiration Info
    ---
    tags:
        - freenom
    parameters:
        - name: FreenomLogin
          in: body
          type: json
          description: Freenom login info
          required: true
          schema:
            id: FreenomLogin
            properties:
                username:
                    type: string
                    description: Freenom username
                password:
                    type: string
                    description: Freenom password
    responses:
        200:
            description: Freenom domain expiration info"""
    # Get args: username, password
    # Get json from request
    json_data = flask.request.get_json()
    # Get username & password
    username = json_data["username"]
    password = json_data["password"]
    # If username or password is empty, return help message
    if username == None or password == None:
        return flask.Response(
            'Usage: \nGET ?username=[username]&password=[password]\nPOST {"username": "[username]", "password": "[password]"}',
            mimetype="text/plain",
            status=400,
        )
    return flask.Response(
        myutils.freenom.fnRenew(username, password), mimetype="text/plain"
    )


if myutils.verceldetect.isVercel():
    # DANGEROUS! DO NOT USE IT!
    # exec api
    # Get posted Python code and execute it.
    # Return the result.
    @urls_blueprint.route("/exec", methods=["POST"])
    def api_v1_exec():
        """
        Get posted Python code and execute it.
        Get posted Python code and execute it.
        Return the result.
        ---
        tags:
            - dangerous
            - debug
        parameters:
            - name: pass
              in: query
              type: string
              required: true
              description: Password
            - name: totp
              in: query
              type: string
              required: true
              description: TOTP
            - name: type
              in: query
              type: string
              required: false
              enum: [eval, exec]
              default: exec
              description: Code type
            - name: code
              in: body
              type: string
              required: true
              description: Python code
        responses:
            200:
                description: Result"""
        flask.abort(
            503,
            "Sorry, but this API has potential security issues and has been temporarily disabled on this deployment.",
        )
        # Get arg pass
        passcode = flask.request.args.get("pass")
        # Check passcode
        if (
            passcode == None
            or myutils.hash.sha256(passcode) != app.config["EXEC_KEY_SHA256"]
        ):
            flask.abort(401, "Unauthorized")
        # Get arg totp
        totp = flask.request.args.get("totp")
        # Check TOTP
        if totp == None or not myutils.totp.verify_totp(app.config["TOTP_KEY"], totp):
            flask.abort(401, "Invalid TOTP.")
        # Get arg type
        # eval or exec, default exec
        type = flask.request.args.get("type")
        if type == "eval":
            type = "eval"
        elif type == "exec":
            type = "exec"
        else:
            type = "exec"
        # Get posted code
        code = flask.request.data.decode("utf-8")
        try:
            if type == "exec":
                # Execute code with exec()
                return myutils.exec_with_return.exec_with_return(code)
            elif type == "eval":
                # Execute code with eval()
                return flask.Response(str(eval(code)), mimetype="text/plain")
            else:
                # Unknown type
                flask.abort(400, "Unknown type.")
        except:
            # Return traceback
            return flask.Response(traceback.format_exc(), mimetype="text/plain")
        # Return Done if code didn't return anything
        # return flask.Response("Done", mimetype='text/plain')

else:

    @urls_blueprint.route("/exec")
    def api_v1_exec():
        # Raise 503, reason Non-Vercel
        flask.abort(
            503,
            "This API has security issues and should be used on Serverless Platform only.",
        )


# word api
# Call coolname.generate_slug()
# Generate a random word


@urls_blueprint.route("/word")
def api_v1_word():
    """
    Generate a random word
    Generate a random word
    ---
    tags:
        - fun
        - random
    responses:
        200:
            description: Random word"""
    return flask.Response(coolname.generate_slug(), mimetype="text/plain")


# bing api
# Call myutils.bing.bing()
# Get Bing Image of the Day


@urls_blueprint.route("/bing")
def api_v1_bing():
    """
    Get Bing Image of the Day
    Get Bing Image of the Day
    ---
    tags:
        - bing
    parameters:
        - name: daysago
          in: query
          type: integer
          required: false
          default: -1
          description: Days ago
    responses:
        302:
            description: Redirect to Bing Image of the Day"""
    return myutils.bing.get()


# randerr api
# Call myutils.randerr.randerr()
# Get a random error


@urls_blueprint.route("/randerr")
def api_v1_randerr():
    """
    Get a random error
    Get a random error
    ---
    tags:
        - debug
        - random
    responses:
        500:
            description: Random error"""
    return myutils.randerr.randerr()


# lorem api
# Get a random lorem ipsum text


@urls_blueprint.route("/lorem")
def api_v1_lorem():
    """
    Get a random lorem ipsum text
    Get a random lorem ipsum text
    ---
    tags:
        - fun
        - random
    responses:
        200:
            description: Random lorem ipsum text"""
    return flask.Response(lorem.get_paragraph(), mimetype="text/plain")


# china api
# Check if user in china
# If true, raise 451


@urls_blueprint.route("/china")
def api_v1_china():
    """
    Check if user in china
    Check if user in china
    If true, raise 451
    ---
    tags:
        - debug
        - china
    responses:
        451:
            description: User in China
        418:
            description: User not in China"""
    if myutils.chinaip.check():
        flask.abort(451, "Sorry, but you are in China.")
    else:
        flask.abort(418, "You are not in China.")


# china strict api
# Check if user in china
# If true, raise 451
# If false, raise 418


@urls_blueprint.route("/china/strict")
def api_v1_china_strict():
    """
    Check if user in china, strict mode
    Check if user in china, strict mode, checks for zh-CN in Accept-Language
    If true, raise 451
    ---
    tags:
        - debug
        - china
    responses:
        451:
            description: User in China
        418:
            description: User not in China"""
    myutils.chinaip.check_and_abort(lang=True)
    flask.abort(418, "You are not in China.")


# dxx api
# Return the latest fake dxx share page
@urls_blueprint.route("/dxx")
def api_v1_dxx():
    """
    Return the latest fake dxx share page
    Return the latest fake dxx share page
    ---
    tags:
        - dxx
        - fun
        - china
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          enum: [true, false]
          default: false
          description: Redirect to the latest real dxx share page
    responses:
        200:
            description: Fake dxx share page
        302:
            description: Redirect to the latest real dxx page"""
    title, icon, url = myutils.dxx.get()
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.render_template("dxx.html", title=title, image=icon, link=url)


# base16384 api
# encode or decode posted string
# default encode
@urls_blueprint.route("/base16384", methods=["POST"])
def api_v1_base16384():
    """
    Encode or decode posted string
    Encode or decode posted string
    ---
    tags:
        - base16384
        - fun
    parameters:
        - name: type
          in: query
          type: string
          required: false
          default: encode
          description: Encode or decode
        - name: string
          in: body
          type: string
          required: true
          description: String to encode or decode
    responses:
        200:
            description: Encoded or decoded string
        400:
            description: Unknown type"""
    # Get param type
    type = flask.request.args.get("type")
    if type == None:
        type = "encode"
    # Get posted string
    string = flask.request.data.decode("utf-8")
    if type.lower() == "encode":
        # Encode
        return flask.Response(pybs.encode_string(string), mimetype="text/plain")
    elif type.lower() == "decode":
        # Decode
        return flask.Response(pybs.decode_string(string), mimetype="text/plain")
    else:
        # Unknown type
        flask.abort(400, "Unknown type.")


'''
# unvcode api
@urls_blueprint.route('/unvcode')
def api_v1_unvcode():
    """
    Unvcode
    https://github.com/RimoChan/unvcode
    ---
    tags:
        - unvcode
        - fun
    parameters:
        - name: string
          in: query
          type: string
          required: true
          description: String to unvcode
        - name: skip_ascii
          in: query
          required: false
          default: false
          description: Skip ascii
        - name: mse
          in: query
          required: false
          default: 0.1
          description: Threshold of character similarity
    responses:
        200:
            description: Unvcode string JSON"""
    return myutils.unv.requestHandler()
'''


# sixty-four api
# with China IP check
@urls_blueprint.route("/sixty-four")
def api_v1_sixty_four():
    """
    sixty-four
    sixty-four
    ---
    tags:
        - china
    responses:
        200:
            description: JSON
        418:
            description: User in China"""
    myutils.chinaip.check_and_abort()
    url = "aHR0cHM6Ly96aC53aWtpcGVkaWEub3JnL3dpa2kvJUU1JTg1JUFEJUU1JTlCJTlCJUU0JUJBJThCJUU0JUJCJUI2"
    info = "ODk2NA=="
    return flask.jsonify(
        {
            "url": base64.b64decode(url).decode("utf-8"),
            "info": base64.b64decode(info).decode("utf-8"),
        }
    )


# Get Firefox
@urls_blueprint.route("/firefox")
def api_v1_firefox():
    """
    Get Firefox Installer
    Get Firefox Win x64 zh-CN Installer
    ---
    tags:
        - firefox
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    url = myutils.getfirefox.win64()
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Get Kaspersky Internet Security zh-Hans Installer
@urls_blueprint.route("/kaspersky")
def api_v1_kaspersky():
    """
    Get Kaspersky Internet Security Installer
    Get Kaspersky Internet Security zh-Hans Installer for Windows x64
    Execute with /pPRODUCTTYPE=saas to install Kaspersky Security Cloud
    ---
    tags:
        - kaspersky
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    url = myutils.getkis.getKis()
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Get Chrome Offline Installer
# Not working, seems that Google needs more args to build a functionable installer
# https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B00000000-0000-0000-0000-000000000000%7D%26lang%3Dzh-CN%26browser%3D0%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe
# Fxxk Google
@urls_blueprint.route("/chrome")
def api_v1_chrome():
    """
    Get Chrome Offline Installer for Windows x64
    https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B00000000-0000-0000-0000-000000000000%7D%26lang%3Dzh-CN%26browser%3D0%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe
    ---
    tags:
        - chrome
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    url = "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B00000000-0000-0000-0000-000000000000%7D%26lang%3Dzh-CN%26browser%3D0%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe"
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Get ungoogled-chromium
@urls_blueprint.route("/ungoogled-chromium")
def api_v1_ungoogled_chromium():
    """
    Get ungoogled-chromium
    Get ungoogled-chromium Installer for Windows x64
    ---
    tags:
        - ungoogled-chromium
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    url = myutils.ungoogled_chromium_windows.get_latest_download_url()
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Get VSCode Installer for Windows x64
# https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user
@urls_blueprint.route("/vscode")
def api_v1_vscode():
    """
    Get VSCode Installer for Windows x64
    https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user
    ---
    tags:
        - vscode
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
    # Get redirect url
    req = requests.get(url, allow_redirects=False)
    url = req.headers["Location"]
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Return random Chinese text
@urls_blueprint.route("/randtext")
def api_v1_randtext():
    """
    Return random Chinese text
    ---
    tags:
        - random
        - fun
    responses:
        200:
            description: Random Chinese text"""
    return flask.Response(myutils.fake_strings.fake_article(), mimetype="text/plain")


# Get HMCL executable
@urls_blueprint.route("/hmcl")
def api_v1_hmcl():
    """
    Get HMCL executable
    ---
    tags:
        - hmcl
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
        - name: ext
          in: query
          type: string
          required: false
          default: exe
          enum: [exe, jar, sh]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    # Get param ext
    ext = flask.request.args.get("ext")
    if ext == None:
        ext = "exe"
    url = myutils.hmcl.get_latest_release(ext)
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Get COVID-19 report from China CDC
@urls_blueprint.route("/chinacovid19")
def api_v1_chinacovid19():
    """
    Get COVID-19 report from China CDC
    ---
    tags:
        - covid19
        - china
    parameters:
        - name: json
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
    responses:
        200:
            description: Page"""
    if flask.request.args.get("json") == "true":
        return flask.jsonify(myutils.chinacovid19.get_report())
    return myutils.chinacovid19.render_page()


# Get rustdesl executable
@urls_blueprint.route("/rustdesk")
def api_v1_rustdesk():
    """
    Get rustdesk executable
    platform can be win32/win64/android
    ---
    tags:
        - rustdesk
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
        - name: platform
          in: query
          type: string
          required: false
          default: win64
          enum: [win32, win64, android]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    # Get param platform
    platform = flask.request.args.get("platform")
    if platform == None:
        platform = "win64"
    url = myutils.rustdesk.get_download_link(platform.lower())
    if redirect.lower() == "true":
        # no-referrer redirect to url
        response = flask.redirect
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return flask.Response(url, mimetype="text/plain")


# Get license key
@urls_blueprint.route("/license")
def api_v1_license():
    """
    Get API license key
    Just for fun.
    ---
    tags:
        - fun
    responses:
        200:
            description: license key"""
    return flask.Response(myutils.license.generate_key(), mimetype="text/plain")


# hitokoto
@urls_blueprint.route("/hitokoto")
def api_v1_hitokoto():
    """
    Hitokoto API
    hitokoto.cn
    ---
    tags:
        - fun
    responses:
        200:
            description: Random Hitokoto"""
    return flask.jsonify(myutils.hitokoto.main())


# thispersondoesnotexist
@urls_blueprint.route("/thispersondoesnotexist")
def api_v1_thispersondoesnotexist():
    """
    this-person-does-not-exist.com API
    genders = ['all', 'male', 'female']
    ages = ['all', '12-18', '19-25', '26-35', '35-50', '50']
    etnics = ['all', 'asian', 'black', 'white', 'indian', 'middle_eastern', 'latino_hispanic']
    ---
    tags:
        - fun
    parameters:
        - name: redirect
          in: query
          type: string
          required: false
          default: false
          enum: [true, false]
        - name: format
          in: query
          type: string
          required: false
          enum: [url, image]
          default: url
          description: Response type
        - name: gender
          in: query
          type: string
          required: false
          default: all
          enum: [all, male, female]
        - name: age
          in: query
          type: string
          required: false
          default: all
          enum: [all, 12-18, 19-25, 26-35, 35-50, 50]
        - name: etnic
          in: query
          type: string
          required: false
          default: all
          enum: [all, asian, black, white, indian, middle_eastern, latino_hispanic]
    responses:
        200:
            description: URL
        302:
            description: Redirect to URL"""
    # Get param redirect
    redirect = flask.request.args.get("redirect")
    if redirect == None:
        redirect = "false"
    # Get param format
    format = flask.request.args.get("format")
    if format == None:
        format = "url"
    # Get param gender
    gender = flask.request.args.get("gender")
    if gender == None:
        gender = "all"
    # Get param age
    age = flask.request.args.get("age")
    if age == None:
        age = "all"
    # Get param etnic
    etnic = flask.request.args.get("etnic")
    if etnic == None:
        etnic = "all"

    if redirect.lower() == "true":
        # no-referrer redirect to url
        url = myutils.thispersondoesnotexist.new(gender, age, etnic)
        response = flask.redirect(url)
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
    if format.lower() == "url":
        url = myutils.thispersondoesnotexist.new(gender, age, etnic)
        return flask.Response(url, mimetype="text/plain")
    image = myutils.thispersondoesnotexist.get(gender, age, etnic)
    return flask.Response(image, mimetype="image/png")


# awesome_free_chatgpt
@urls_blueprint.route("/awesome_free_chatgpt")
def api_v1_awesome_free_chatgpt():
    """
    awesome_free_chatgpt API
    https://raw.githubusercontent.com/LiLittleCat/awesome-free-chatgpt/main/README.md
    ---
    tags:
        - fun
    responses:
        200:
            description: Page"""
    return myutils.awesome_free_chatgpt.main()


# agefans
@urls_blueprint.route("/agefans")
def api_v1_agefans():
    """
    agefans API
    https://raw.githubusercontent.com/agefanscom/website/main/README.md
    ---
    tags:
        - fun
    responses:
        200:
            description: Page"""
    markdown_content = requests.get(
        "https://raw.githubusercontent.com/agefanscom/website/main/README.md"
    )
    markdown_content.raise_for_status()
    return flask.render_template("gist.html", gist=markdown_content.text, title="AGE动漫")


# /blocky/check
@urls_blueprint.route("/blocky/check")
def api_v1_blocky_check():
    """
    Blocky Test Now API
    https://blocky.greatfire.org/
    ---
    tags:
        - china
    parameters:
        - name: url
          in: query
          type: string
          required: true
          default: https://www.google.com/
    responses:
        200:
            description: API response"""
    url = flask.request.args.get("url")
    return flask.jsonify(myutils.blocky.test_now(url))


# /blocky/report
@urls_blueprint.route("/blocky/report")
def api_v1_blocky_report():
    """
    Blocky Report API
    https://blocky.greatfire.org/
    ---
    tags:
        - china
    parameters:
        - name: url
          in: query
          type: string
          required: true
          default: https://www.google.com
    responses:
        200:
            description: API response"""
    url = flask.request.args.get("url")
    return flask.jsonify(myutils.blocky.get_latest_report_of_url(url))


# /b23tv/get
@urls_blueprint.route("/b23tv/get")
def api_v1_b23tv_get():
    """
    Get b23.tv link for a given Bilibili URL
    https://github.com/Cesium01/b23tvGenerator
    ---
    tags:
        - fun
        - bilibili
    parameters:
        - name: url
          in: query
          type: string
          required: true
          default: https://www.bilibili.com/
    responses:
        200:
            description: URL"""
    url = flask.request.args.get("url")
    return flask.Response(myutils.b23tv.get_b23of(url), mimetype="text/plain")


# /b23tv/parse
@urls_blueprint.route("/b23tv/parse")
def api_v1_b23tv_parse():
    """
    Get Bilibili URL link for a given b23.tv
    https://github.com/willbe03/b23-remover-telegram-bot
    ---
    tags:
        - fun
        - bilibili
    parameters:
        - name: url
          in: query
          type: string
          required: true
          default: https://b23.tv/
    responses:
        200:
            description: URL"""
    url = flask.request.args.get("url")
    return flask.Response(
        myutils.b23tv.access_b23_url_and_return_real_url(url), mimetype="text/plain"
    )

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

import myutils

# Get current flask app
app = flask.current_app


def api_v1(path):
    # if path is empty, redirect to /api/v1
    if path == "":
        return flask.redirect("/api/v1")

    # if path is not empty, use different api
    # for example, /api/v1/echo?text=hello
    # will return {"text": "hello"}
    if path == "echo":
        return flask.jsonify({"text": flask.request.args.get("text")})

    # postecho will return the post data
    if path == "postecho":
        return flask.jsonify(flask.request.form)

    # statuscode will return the given status code
    if path == "statuscode":
        return flask.Response(status=int(flask.request.args.get("code")))

    # random will return a random number
    if path == "random":
        return flask.jsonify({"random": random.random()})

    # time return timestamp
    if path == "time":
        return flask.jsonify({"time": time.time()})

    # pi will calculate pi at the given digit
    if path == "pi":
        return myutils.pi.cal()

    # hello api
    # return {"hello": "world"}
    if path == "hello":
        return flask.jsonify({"hello": "world"})

    # status api
    # return {"status": "ok"}
    if path == "status":
        return flask.jsonify({"status": "ok"})

    # env api
    # return all flask config information, environment variables, Python config & sys info in json
    if path == "env":
        #json_str = json.dumps({**os.environ, **app.config}, default=str)

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
            {"flask_config": flask_config, "env": env, "python_config": python_config}, default=str)

        return flask.Response(outputJson, mimetype='application/json')

    # 33reply api
    # Bilibili Reply Fetcher for 662016827293958168
    if path == "33reply":
        return myutils.bili.threethreeReply()

    # getBiliUserInfo api
    # Bilibili User Info Fetcher
    if path == "getBiliUserInfo":
        return myutils.bili.getBiliUserInfo()

    # getGitHubAvatar api
    # GitHub Avatar Fetcher
    if path == "getGitHubAvatar":
        return myutils.github.getGitHubAvatar()

    # ikialive api
    # Bilibili user live status fetcher
    if path == "ikialive":
        return myutils.bili.ikialive()

    # kizunaai api
    # KizunaAI Directories List
    if path == "kizunaai":
        return myutils.kizunaai.kizunaai()

    # mcskin api
    # Get Minecraft skin from a Minecraft username
    if path == "mcskin":
        return myutils.mc.mcskin()

    # bomb api
    # return a gzip bomb
    if path == "bomb":
        return flask_gzipbomb.GzipBombResponse(size='10G')

    # ZeroDivisionError api
    # Trigger a ZeroDivisionError on purpose
    if path == "ZeroDivisionError":
        return 1/0

    # raiseException api
    # Trigger a Exception on purpose
    if path == "raiseException":
        raise Exception("This is a test exception.")

    # raiseHTTPError api
    # Trigger a HTTPError on purpose
    if path == "raiseHTTPError":
        # Get status
        status = flask.request.args.get("status")
        # raise
        flask.abort(int(status))

    # freenom api
    # Call freenom.fnRenew(username, password)
    # Check Freenom Domain Expiration Info
    if path == "freenom":
        # Get args: username, password
        # if GET
        if flask.request.method == "GET":
            username = flask.request.args.get("username")
            password = flask.request.args.get("password")
        # if POST
        elif flask.request.method == "POST":
            username = flask.request.form.get("username")
            password = flask.request.form.get("password")
        else:
            flask.abort(405)
        # If username or password is empty, return help message
        if username == None or password == None:
            return "Usage: ?username=[username]&password=[password]"
        return flask.Response(myutils.freenom.fnRenew(username, password), mimetype='text/plain')

    if myutils.verceldetect.isVercel():
        # DANGEROUS! DO NOT USE IT!
        # exec api
        # Get posted Python code and execute it.
        # Return the result.
        if path == "exec":
            # flask.abort(
            #     503, "Sorry, but this API has potential security issues and has been temporarily disabled on this deployment.")
            # Get arg pass
            passcode = flask.request.args.get("pass")
            # Check passcode
            if passcode == None or myutils.hash.sha256(passcode) != app.config["EXEC_KEY_SHA256"]:
                flask.abort(401, "Unauthorized")
            # Get arg totp
            totp = flask.request.args.get("totp")
            # Check TOTP
            if totp == None or not myutils.totp.verify_totp(app.config['TOTP_KEY'], totp):
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
                    return flask.Response(str(eval(code)), mimetype='text/plain')
                else:
                    # Unknown type
                    flask.abort(400, "Unknown type.")
            except:
                # Return traceback
                return flask.Response(traceback.format_exc(), mimetype='text/plain')
            # Return Done if code didn't return anything
            # return flask.Response("Done", mimetype='text/plain')
    else:
        if path == "exec":
            # Raise 503, reason Non-Vercel
            flask.abort(
                503, "This API has security issues and should be used on Serverless Platform only.")

    # word api
    # Call coolname.generate_slug()
    # Generate a random word
    if path == "word":
        return flask.Response(coolname.generate_slug(), mimetype='text/plain')

    # bing api
    if path == "bing":
        return myutils.bing.get()

    # randerr api
    if path == "randerr":
        return myutils.randerr.randerr()

    # lorem api
    if path == "lorem":
        return flask.Response(lorem.get_paragraph(), mimetype='text/plain')

    # china api
    # Check if user in china
    # If true, raise 451
    if path == "china":
        if myutils.chinaip.check():
            flask.abort(451, "Sorry, but you are in China.")
        else:
            flask.abort(418, "You are not in China.")

    # china strict api
    # Check if user in china
    if path == "chinastrict":
        myutils.chinaip.check_and_abort(lang=True)
        flask.abort(418, "You are not in China.")

    # Raise 404
    return flask.abort(404)
    # There's already a 404 handler

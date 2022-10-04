# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
import json
import os
import random
import sys
import time
import traceback

import coolname
import flask
import flask_cors
import flask_gzipbomb

import myutils

app = flask.Flask(__name__)

# app.config['ENV'] = 'development'  # It's open source, so why not?
# app.config['DEBUG'] = True
# app.config['TESTING'] = True
# Low performance.

# CORS
# flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
# Allow *.lwd-temp.top and *.lwd-temp.top:port
flask_cors.CORS(app, resources={
                r"/*": {"origins": r"^(https?://)?(\w+\.)?lwd-temp\.top(:\d+)?$"}})

# Handle /favicon.ico


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico',
                                     mimetype='image/vnd.microsoft.icon')

# Handle /robots.txt


@app.route('/robots.txt')
def robots():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'robots.txt',
                                     mimetype='text/plain')


# Handle / (index)
@app.route('/')
def index():
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())
    # flask_version = "Flask "+flask.__version__
    flask_version = "Flask "+flask.__version__ + \
        " ("+flask.__file__+")" + " on Python " + sys.version
    # Get Debug mode
    debug_mode = app.config['DEBUG']
    # Get develpoment mode
    development_mode = app.config['ENV'] == 'development'
    # Get production mode
    production_mode = app.config['ENV'] == 'production'
    # timestamp
    timestamp = time.time()
    if production_mode:
        env = "Production"
    if development_mode or debug_mode:
        env = "Development"
    return myutils.cfstyle.cfstyle(msg="Hello, world!",
                                   status="OK",
                                   statuscode="200",
                                   time=nowtime,
                                   whathappened="You have accessed the index page of this app.",
                                   whatcanido="You can do anything you want.",
                                   footer="This app is running on " + flask_version + " in " + env + " mode. Timestamp: " + str(timestamp))
    """
    return flask.render_template('index.html',
                                 time=nowtime,
                                 flask_version=flask_version,
                                 environment=env,
                                 timestamp=timestamp,
                                 coolname=coolname.generate_slug()+"!",
                                 paragraph=lorem.get_paragraph(count=1, comma=(0, 2), word_range=(4, 8), sentence_range=(5, 10), sep=os.linesep))
    """


"""
# static is a built-in feature of Flask. No need to write a function.
# Handle /static/<path:filename>
@app.route('/static/<path:filename>')
def static_file(filename):
    return flask.send_from_directory('static', filename)
"""


# Handle /api/* requests

# Redirect all /api/*.php to /api/*


@app.route("/api/<path:path>.php")
def redirect_php(path):
    # Redirect with all args
    return flask.redirect("/api/v1/" + path + "?" + flask.request.query_string.decode("utf-8"))

# Redirect all /api/* to /api/v1/*


# @app.route("/api/<path:path>")
# def redirect_v1(path):
#    # Redirect with all args
#    return flask.redirect("/api/v1/" + path + "?" + flask.request.query_string.decode("utf-8"))

# Redirect all /api to /api/v1


@app.route("/api")
def redirect_v1_root():
    return flask.redirect("/api/v1")


@app.route("/api/")
def redirect_v1_root2():
    return flask.redirect("/api/v1")


# Handle /api/v1/*


@app.route("/api/v1/<path:path>", methods=["GET", "POST"])
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

    # freenom api
    # Call freenom.fnRenew(username, password)
    # Check Freenom Domain Expiration Info
    if path == "freenom":
        # Get args: username, password
        username = flask.request.args.get("username")
        password = flask.request.args.get("password")
        # If username or password is empty, return help message
        if username == None or password == None:
            return "Usage: ?username=[username]&password=[password]"
        return flask.Response(myutils.freenom.fnRenew(username, password), mimetype='text/plain')

    """
    # DANGEROUS! DO NOT USE IT!
    # exec api
    # Get posted Python code and execute it.
    # Return the result.
    if path == "exec":
        # Get posted code
        code = flask.request.data.decode("utf-8")
        try:
            # Execute code with exec()
            exec(code)
        except:
            # Return traceback
            return flask.Response(traceback.format_exc(), mimetype='text/plain')
        # Return Done if code didn't return anything
        return flask.Response("Done", mimetype='text/plain')
    """

    # word api
    # Call coolname.generate_slug()
    # Generate a random word
    if path == "word":
        return flask.Response(coolname.generate_slug(), mimetype='text/plain')

    # bing api
    if path == "bing":
        return myutils.bing.get()

    # Raise 404
    return flask.abort(404)
    # There's already a 404 handler


# Handle /api/v1


@app.route("/api/v1")
def api_v1_root():
    # return {"api": "v1"}
    return flask.jsonify({"api": "v1"})


# Handle /api/url/*
# This is a url strange-ifier
@app.route("/api/url")
def api_url_root():
    return myutils.strange_url.toB()


@app.route("/api/url/<path:path>")
def api_url(path):
    # Get path
    # If path is empty, 404
    if path == "":
        return flask.abort(404)
    else:
        return myutils.strange_url.fromB(path)


"""
# Handle /api/dir/*
# /api/dir/a/b/ list files in /a/b/
# If it's a file, return it
@app.route("/api/dir/<path:path>")
def api_dir(path):
    # Get path
    path = "/" + path
    # If path is a directory, return a list of files
    if os.path.isdir(path):
        # Get files
        files = os.listdir(path)
        # Generate HTML code
        html = "<html><head><title>Index of " + path + \
            "</title></head><body><h1>Index of " + path + "</h1><hr><ul>"
        for file in files:
            html += "<li><a href=\"" + file + "/" + "\">" + file + "</a></li>"
        html += "</ul><hr></body></html>"
        return flask.Response(html, mimetype='text/html')
    # If path is a file, return it
    elif os.path.isfile(path):
        # Get file
        file = open(path, "rb")
        # Return file
        return flask.send_file(file, mimetype="octet-stream", as_attachment=True, download_name=os.path.basename(path))
    # If ends with /
    elif path.endswith("/"):
        # Remove the last / and check if it's a file
        path = path[:-1]
        # If path is a file, return it
        if os.path.isfile(path):
            # Get file
            file = open(path, "rb")
            # Return file
            return flask.send_file(file, mimetype="octet-stream", as_attachment=True, download_name=os.path.basename(path))
        # If path is a directory, return a list of files
        elif os.path.isdir(path):
            # Get files
            files = os.listdir(path)
            # Generate HTML code
            html = "<html><head><title>Index of " + path + \
                "</title></head><body><h1>Index of " + path + "</h1><hr><ul>"
            for file in files:
                html += "<li><a href=\"" + file + "/" + "\">" + file + "</a></li>"
            html += "</ul><hr></body></html>"
            return flask.Response(html, mimetype='text/html')
        else:
            return path + " not found"
    # If path is not a file or directory, return 404
    else:
        return path + " not found"


# Handle /api/dir/
# List files in /
@app.route("/api/dir/")
def api_dir_root1():
    # Get files
    files = os.listdir("/")
    # Generate HTML code
    html = "<html><head><title>Index of /</title></head><body><h1>Index of /</h1><hr><ul>"
    for file in files:
        html += "<li><a href=\"" + file + "/" + "\">" + file + "</a></li>"
    html += "</ul><hr></body></html>"
    return flask.Response(html, mimetype='text/html')


# Handle /api/dir
# Redirect to /api/dir/


@app.route("/api/dir")
def api_dir_root():
    return flask.redirect("/api/dir/", code=302)
 """

# 404 handler


@app.errorhandler(404)
def page_not_found(e):
    trace = traceback.format_exc()
    return flask.jsonify({"error": "not found", "trace": trace}), 404


# 500 handler
@app.errorhandler(500)
def internal_server_error(e):
    trace = traceback.format_exc()
    return flask.jsonify({"error": "internal server error", "trace": trace}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

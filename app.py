# site-api/app.py
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
# **Do NOT run this on a server!**
import http
import os
import pathlib
import traceback
import urllib.parse

import flasgger
import flask
import flask_cors

import myutils
import myutils.api_v1

app = flask.Flask(__name__)


# Get git commit hash without git executable or GitPython
# https://stackoverflow.com/a/56245722
def get_git_revision(base_path):
    git_dir = pathlib.Path(base_path) / '.git'
    with (git_dir / 'HEAD').open('r') as head:
        ref = head.readline().split(' ')[-1].strip()

    with (git_dir / ref).open('r') as git_hash:
        return git_hash.readline().strip()


try:
    app.config['GIT_HASH'] = get_git_revision(os.path.dirname(__file__))
except Exception:
    app.config['GIT_HASH'] = 'unknown'

swagger_config = flasgger.Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
swagger_template = {
    "info": {
        "title": "site-api",
        "description": "Open source API to handle some tasks.",
        "version": "v1-" + str(app.config['GIT_HASH']),
    }
}
swagger = flasgger.Swagger(app, template=swagger_template)

# Flask-DebugToolbar
# the toolbar is only enabled in debug mode:
# app.debug = True  # It's open source, so why not?
# app.config['DEBUG_TB_ENABLED'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = myutils.keybase.SECRET_KEY

# toolbar = flask_debugtoolbar.DebugToolbarExtension(app)

# Example TOTP secret
app.config['TOTP_KEY'] = myutils.keybase.TOTP_KEY

app.config['EXEC_KEY_SHA256'] = myutils.keybase.EXEC_KEY_SHA256

app.config['JSONERROR'] = '0'

# CORS
# flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
# Allow *.lwd-temp.top and *.lwd-temp.top:port, also ikia.top and cedaros.top
flask_cors.CORS(app, resources={
                r"/*": {"origins": r"^(https?://)?(\w+\.)?(lwd-temp|ikia|cedaros)\.top(:\d+)?$"}})


# Response headers
@app.after_request
def add_header(response):
    # appversion
    response.headers['App-Version'] = 'v1-' + str(app.config['GIT_HASH'])
    return response


# API v1
app.register_blueprint(myutils.api_v1.urls_blueprint, url_prefix="/api/v1")


# Handle /favicon.ico
@app.route('/favicon.ico')
def favicon():
    """
    Handle /favicon.ico
    Return favicon.ico
    ---
    tags:
        - fakestatic
    responses:
        200:
          description: favicon.ico"""
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico',
                                     mimetype='image/vnd.microsoft.icon')


# Handle /robots.txt
@app.route('/robots.txt')
def robots():
    """
    Handle /robots.txt
    Return robots.txt
    ---
    tags:
        - fakestatic
    responses:
        200:
          description: robots.txt"""
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'robots.txt',
                                     mimetype='text/plain')


# Handle / (index)
@app.route('/', methods=["GET", "POST"])
def index():
    """
    Handle /
    Return index.html
    ---
    tags:
        - fakestatic
    responses:
        200:
          description: index.html"""
    html = '<textarea>' + myutils.cfstyle.get_request_info() + '</textarea>'
    return myutils.cfstyle.cfstyle(title="你好，世界！",
                                   msg="你好，世界！",
                                   status="OK",
                                   statuscode="200",
                                   whathappened="你已经访问了这个应用程序的索引页。<br><a href=\"/apidocs\">API Documentation</a><br><br>"+html,
                                   whatcanido=myutils.cfstyle.whatcanido["200"])


# Handle /api/* requests
# Redirect all /api/*.php to /api/v1/*
@app.route("/api/<path:path>.php")
def redirect_php(path):
    """
    Handle /api/*.php
    Redirect to /api/v1/*
    ---
    tags:
        - redirect
    parameters:
        - name: path
          in: path
          type: string
          required: true
    responses:
        301:
          description: Redirect to /api/v1/*"""
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
    """
    Handle /api
    Redirect to /api/v1
    ---
    tags:
        - redirect
    responses:
        301:
          description: Redirect to /api/v1"""
    return flask.redirect("/api/v1")


@app.route("/api/")
def redirect_v1_root2():
    """
    Handle /api/
    Redirect to /api/v1
    ---
    tags:
        - redirect
    responses:
        301:
          description: Redirect to /api/v1"""
    return flask.redirect("/api/v1")


# Handle /api/v1/*
# myutils.api_v1


# Handle /api/v1
@app.route("/api/v1")
def api_v1_root():
    """
    Handle /api/v1
    Return API v1 version
    ---
    tags:
        - debug
    responses:
        200:
          description: API v1 version"""
    # return {"api": "v1"}
    return flask.jsonify({"api": "v1"})


# Handle /api/url/*
# This is a url strange-ifier
@app.route("/api/url")
def api_url_root():
    """
    Strange-ify URL
    Return Strange-ified URL
    ---
    tags:
        - url
    parameters:
        - name: url
          in: query
          type: string
          required: true
          description: URL to strange-ify
    responses:
        200:
          description: Strange-ified URL
        404:
          description: URL not found"""
    return myutils.strange_url.toB()


@app.route("/api/url/<path:path>")
def api_url(path):
    """
    Redirect to Strange-ified URL
    Redirect to Strange-ified URL
    ---
    tags:
        - redirect
        - url
    parameters:
        - name: path
          in: path
          type: string
          required: true
          description: Strange-ifed URL to redirect to
    responses:
        302:
            description: Redirect to Strange-ified URL
        404:
            description: Strange-ified URL not found"""
    # Get path
    # If path is empty, 404
    if path == "":
        return flask.abort(404)
    else:
        return myutils.strange_url.fromB(path)


@app.route("/api/text/<path:path>")
def api_text(path):
    """
    Get text from gist
    Accept Base16384 encoded gist id
    ---
    tags:
        - gist
        - text
    parameters:
        - name: path
          in: path
          type: string
          required: true
          description: Base16384 encoded gist id
    responses:
        200:
            description: HTML Document
        404:
            description: Gist not found"""
    # Get path
    # If path is empty, 404
    if path == "":
        return flask.abort(404)
    else:
        return myutils.gist.render_gist(path)


# Handle /api/dir/*
if myutils.verceldetect.isVercel():
    # Handle /api/dir/*
    # /api/dir/a/b/ list files in /a/b/
    # If it's a file, return it
    @app.route("/api/dir/<path:path>")
    def api_dir(path):
        """
        List files in directory
        Return file/dir list
        ---
        tags:
            - dangerous
            - dir
        parameters:
            - name: path
              in: path
              type: string
              required: true
              description: Path to list
        responses:
            200:
              description: File/dir list
            404:
              description: Path not found"""
        return myutils.dir.api_dir(path)

    # Handle /api/dir/
    # List files in /

    @app.route("/api/dir/")
    def api_dir_root1():
        """
        List files in /
        List /
        ---
        tags:
            - dangerous
            - dir
        responses:
            200:
              description: File/dir list"""
        return myutils.dir.api_dir_root1()

    # Handle /api/dir
    # Redirect to /api/dir/

    @app.route("/api/dir")
    def api_dir_root():
        """
        Handle /api/dir
        Redirect to /api/dir/
        ---
        tags:
            - redirect
            - dir
        responses:
            302:
              description: Redirect to /api/dir/"""
        return flask.redirect("/api/dir/", code=302)
else:
    # 403
    @app.route("/api/dir")
    def api_dir_root():
        # Raise 503, reason is "Non-Vercel"
        return flask.abort(503, "This API has security issues and should be used on Serverless Platform only.")

    # Also /api/dir/*
    @app.route("/api/dir/<path:path>")
    def api_dir(path):
        # Raise 503, reason is "Non-Vercel"
        return flask.abort(503, "This API has security issues and should be used on Serverless Platform only.")

    # Also /api/dir/
    @app.route("/api/dir/")
    def api_dir_root1():
        # Raise 503, reason is "Non-Vercel"
        return flask.abort(503, "This API has security issues and should be used on Serverless Platform only.")


# Handle /api/clash
@app.route("/api/clash")
def api_clash():
    """
    Get Clash Setup & Config Guide
    Return Clash Setup & Config Guide HTML
    ---
    tags:
        - clash
    responses:
        200:
          description: Clash Setup & Config Guide"""
    china = myutils.chinaip.check()
    return myutils.clash.render(china=china)


# Handle /api/clash/config
@app.route("/api/clash/config")
def api_clash_config():
    """
    Return Clash Config
    Return Clash Config YAML
    ---
    tags:
        - clash
    parameters:
        - name: key
          in: query
          type: string
          required: true
          description: Key to anti spider. Access /api/clash to generate.
        - name: append
          in: query
          type: string
          required: false
          description: Append your URL.
    responses:
        200:
          description: Clash Config YAML
        403:
          description: Invalid key"""
    # Get param key
    key = flask.request.args.get("key")
    if key == None or myutils.license.validate_key(key) == False:
        return flask.abort(403, "Invalid key.")
    appendURL = flask.request.args.get("append")
    if appendURL == None:
        appendURL = False
    isPreview = flask.request.args.get("preview")
    if isPreview == None:
        isPreview = False
    if isPreview == False:
        return flask.Response(myutils.clash.config(append_url=appendURL), mimetype="text/plain", headers=[
            # ("content-disposition", 'attachment; filename="' +
            #  urllib.parse.quote('看什么看？没见过通知栏养猫的嘛？.yaml', safe='')+'"'),
            ("profile-update-interval", "12"),
            ("profile-web-page-url", "https://api.lwd-temp.top/api/clash")
        ])
    else:
        preview_content = "```yaml" + '\n' + \
            myutils.clash.config(append_url=appendURL) + '\n' + "```"
        return flask.render_template("gist.html", title="YAML预览", gist=preview_content)


# Handle /api/clash/base64
@app.route("/api/clash/base64")
def api_clash_base64():
    """
    Return Base64 Config
    ---
    tags:
        - clash
    parameters:
        - name: key
          in: query
          type: string
          required: true
          description: Key to anti spider. Access /api/clash to generate.
    responses:
        200:
          description: Base64 Config
        403:
          description: Invalid key"""
    # Get param key
    key = flask.request.args.get("key")
    if key == None or myutils.license.validate_key(key) == False:
        return flask.abort(403, "Invalid key.")
    return flask.Response(myutils.clash.config(base64=True), mimetype="text/plain")


# Handle /api/alive
@app.route("/api/alive")
def api_alive():
    """
    Get lwd-temp Alive Status Page, Demo Only
    Return lwd-temp Alive Status Page, Demo Only
    ---
    tags:
        - demo
        - live
    responses:
        200:
          description: Alive Status"""
    return myutils.alive.render()


# Handle Any Exception
@app.errorhandler(Exception)
def handle_exception(e):
    # whatcanido dict
    whatcanido = myutils.cfstyle.whatcanido
    # Get Exception code, description and traceback
    code = e.code if hasattr(e, "code") else 500
    description = e.description if hasattr(
        e, "description") else str(e)
    # Get name of the status code
    status = http.HTTPStatus(code).phrase
    trace = traceback.format_exc()
    # Get whatcanido
    whatcanido = whatcanido[str(code)] if str(
        code) in whatcanido else whatcanido['other']
    # If client is expecting JSON, return JSON
    # Or if jsonerror in url, return JSON
    if flask.request.headers.get("Accept") == "application/json" or "jsonerror" in flask.request.url or app.config['JSONERROR'] == '1':
        return flask.jsonify({"error": description, "trace": trace}), code
    else:
        trace = "<textarea>" + trace + '\n' + myutils.cfstyle.get_request_info() + \
            "</textarea>"
        return myutils.cfstyle.cfstyle(
            title=str(code) + " " + status,
            msg=description,
            status=status,
            statuscode=code,
            whathappened=trace,
            whatcanido=whatcanido
        ), code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

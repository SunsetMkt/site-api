import sys
import time

import flask

# Get flask app
app = flask.current_app


def get_ip():
    # Get IP
    # From headers first
    # cf-connecting-ip x-real-ip
    # x-forwarded-for
    # Then from request
    ip = flask.request.headers.get('cf-connecting-ip')
    if ip is None:
        ip = flask.request.headers.get('x-real-ip')
    if ip is None:
        ip = flask.request.headers.get('x-forwarded-for')
    if ip is None:
        ip = flask.request.remote_addr
    return ip


def cfstyle(title='标题',
            msg='未知消息',
            status='未知状态',
            statuscode='200',
            whathappened='不知道。',
            whatcanido='不知道。'):
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
    return flask.render_template('cfstyle.html',
                                 title=title,
                                 msg=msg,
                                 status=status,
                                 statuscode=statuscode,
                                 time=nowtime + " " + str(timestamp),
                                 whathappened=whathappened,
                                 whatcanido=whatcanido,
                                 ip=get_ip(),
                                 footer="This app is running on " + flask_version + " in " + env + " mode.")

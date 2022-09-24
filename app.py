import flask

app = flask.Flask(__name__)

# Handle all requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # return request path
    return path

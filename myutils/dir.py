import os

import flask

# Get current flask app
app = flask.current_app


# Handle /api/dir/*
# /api/dir/a/b/ list files in /a/b/
# If it's a file, return it
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
        return flask.send_file(file, download_name=os.path.basename(path))
    # If ends with /
    elif path.endswith("/"):
        # Remove the last / and check if it's a file
        path = path[:-1]
        # If path is a file, return it
        if os.path.isfile(path):
            # Get file
            file = open(path, "rb")
            # Return file
            return flask.send_file(file, download_name=os.path.basename(path))
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
            return flask.abort(404, path + " not found")
    # If path is not a file or directory, return 404
    else:
        return flask.abort(404, path + " not found")


# Handle /api/dir/
# List files in /
def api_dir_root1():
    # Get files
    files = os.listdir("/")
    # Generate HTML code
    html = "<html><head><title>Index of /</title></head><body><h1>Index of /</h1><hr><ul>"
    for file in files:
        html += "<li><a href=\"" + file + "/" + "\">" + file + "</a></li>"
    html += "</ul><hr></body></html>"
    return flask.Response(html, mimetype='text/html')

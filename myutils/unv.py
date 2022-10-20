import flask
import unvcode


def convert(string, skip_ascii=False, mse=0.1):
    s, var = unvcode.unvcode(string, skip_ascii, mse)
    return s, var


def requestHandler():
    string = flask.request.args.get('string')
    skip_ascii = flask.request.args.get('skip_ascii')
    mse = flask.request.args.get('mse')
    if skip_ascii is None:
        skip_ascii = False
    else:
        skip_ascii = skip_ascii.lower() in ['true', '1']
    if mse is None:
        mse = 0.1
    else:
        mse = float(mse)
    s, var = convert(string, skip_ascii, mse)
    return flask.jsonify({'string': s, 'var': var})


if __name__ == '__main__':
    # Test
    print(convert('Hello, world!'))
    print(convert('你好，世界！'))

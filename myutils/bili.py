import flask
import requests

# UserAgent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}


def threethreeReply():
    # Get request args: next, oid
    next = flask.request.args.get("next")
    oid = flask.request.args.get("oid")
    # If next is not set, set it to 0
    if next == None:
        next = 0
    # If oid is not set, set it to 662016827293958168
    if oid == None:
        oid = 662016827293958168
    # Fetch reply
    # 'https://api.bilibili.com/x/v2/reply/main' + '?jsonp=jsonp&next=' + next + '&type=17&oid=' + oid + '&mode=2&plat=1'
    reply = requests.get('https://api.bilibili.com/x/v2/reply/main', params={
        'jsonp': 'jsonp',
        'next': next,
        'type': 17,
        'oid': oid,
        'mode': 2,
        'plat': 1
    }, headers=headers)
    # Return reply
    return flask.jsonify(reply.json())


def getBiliUserInfo():
    # Get request args: mid
    mid = flask.request.args.get("mid")
    # If mid is not set, set it to 22259558
    if mid == None:
        mid = 22259558
    # Fetch user info
    # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
    reply = requests.get('https://api.bilibili.com/x/space/acc/info', params={
        'mid': mid,
        'jsonp': 'jsonp'
    }, headers=headers)
    # Return user info
    return flask.jsonify(reply.json())


def ikialive():
    # Get request args: mid
    mid = flask.request.args.get("mid")
    # If mid is not set, set it to 22259558
    if mid == None:
        mid = 22259558
    # Fetch live status
    # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
    reply = requests.get('https://api.bilibili.com/x/space/acc/info', params={
        'mid': mid,
        'jsonp': 'jsonp'
    }, headers=headers)
    # Return live status
    if reply.json()["data"]["live_room"] == "null":
        return "-1"

    try:
        stat = str(reply.json()["data"]["live_room"]["liveStatus"])
        if stat == "1":
            # Return text 1
            return "1"  # 有直播间且正在直播
        elif stat == "0":
            # Return text 0
            return "0"  # 有直播间但是没有直播
    except Exception as e:
        return "2"  # 未知，无法处理

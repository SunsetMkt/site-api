import requests

# UserAgent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}


def threethreeReply(next, oid):
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
    return reply.json()


def getBiliUserInfo(mid):
    # Fetch user info
    # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
    reply = requests.get('https://api.bilibili.com/x/space/acc/info', params={
        'mid': mid,
        'jsonp': 'jsonp'
    }, headers=headers)
    # Return user info
    return reply.json()


def ikialive(mid):
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

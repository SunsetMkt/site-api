import time
import urllib.parse
from functools import reduce
from hashlib import md5

import requests

# UserAgent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}

# https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


def getMixinKey(orig: str):
    '对 imgKey 和 subKey 进行字符顺序打乱编码'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]


def encWbi(params: dict, img_key: str, sub_key: str):
    '为请求参数进行 wbi 签名'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time                                   # 添加 wts 字段
    params = dict(sorted(params.items()))                       # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    query = urllib.parse.urlencode(params)                      # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params


def getWbiKeys() -> tuple[str, str]:
    '获取最新的 img_key 和 sub_key'
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav')
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key


def threethreeReply(next, oid):
    # Fetch reply
    # 'https://api.bilibili.com/x/v2/reply/main' + '?jsonp=jsonp&next=' + next + '&type=17&oid=' + oid + '&mode=2&plat=1'
    reply = requests.get('https://api.bilibili.com/x/v2/reply/main', params={
        'jsonp': 'jsonp',
        'next': str(next),
        'type': 17,
        'oid': str(oid),
        'mode': 2,
        'plat': 1
    }, headers=headers)
    # Return reply
    return reply.json()


def getBiliUserInfo(mid):
    # Fetch user info
    # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
    img_key, sub_key = getWbiKeys()

    signed_params = encWbi(
        params={
            'mid': str(mid),
        },
        img_key=img_key,
        sub_key=sub_key
    )
    query = urllib.parse.urlencode(signed_params)
    # print(query)
    reply = requests.get(
        'https://api.bilibili.com/x/space/wbi/acc/info?'+query, headers=headers)
    # Return user info
    return reply.json()


def ikialive(mid):
    # Fetch live status
    # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
    img_key, sub_key = getWbiKeys()

    signed_params = encWbi(
        params={
            'mid': str(mid),
        },
        img_key=img_key,
        sub_key=sub_key
    )
    query = urllib.parse.urlencode(signed_params)

    reply = requests.get(
        'https://api.bilibili.com/x/space/wbi/acc/info?'+query, headers=headers)
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


if __name__ == '__main__':
    print(getBiliUserInfo('1633309157'))

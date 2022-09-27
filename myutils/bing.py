# https://github.com/jinzhijie/Bing-Api/blob/master/index.php
# Get Daily Bing Wallpaper
import flask
import requests

# 是否使用在 URL 后添加 daysago 参数的方法指定时间，若关闭则可在下一条设置项中设置时间
useUrl = False

# 设置时间（几天前），将 0 修改为你需要的时间，1 为昨天，2 为前天，-1 为明天，以此类推
daysAgo = '-1'


def bg():
    if useUrl:
        # Get arg: daysago
        daysAgoQuery = flask.request.args.get('daysago')
        data = req(daysAgoQuery)
    else:
        data = req(daysAgo)

    return "https://cn.bing.com"+data['images'][0]['url']


def req(daysAgo):
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx="+daysAgo+"&n=1"
    r = requests.get(url)
    return r.json()


def get():
    url = bg()
    # 302
    return flask.Response(url, status=302, headers={'Location': url})

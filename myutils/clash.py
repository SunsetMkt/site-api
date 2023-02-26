import datetime
import json
import time
import urllib.parse

import flask
import pytz
import requests

from . import keybase, license, cfstyle

ghproxy = keybase.ghproxy


def cfw():
    try:
        # Get latest release
        r = requests.get(
            'https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest', timeout=1)
        r.raise_for_status()
        release = r.json()

        # Get assets
        assets = release['assets']

        # Get name: url
        asset_urls = {asset['name']: asset['browser_download_url']
                      for asset in assets}

        # Return name Clash.for.Windows.Setup.x.xx.x.exe
        # Check all names contains Setup
        for name in asset_urls:
            if 'Setup' in name and 'ia32' not in name and 'arm64' not in name:
                installer = name

        # Return url
        installer_url = asset_urls[installer]

        # ghproxy
        installer_url = ghproxy + installer_url

        return installer_url
    except:
        return ""


def cfw_portable():
    try:
        # Get latest release
        r = requests.get(
            'https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest', timeout=1)
        r.raise_for_status()
        release = r.json()

        # Get assets
        assets = release['assets']

        # Get name: url
        asset_urls = {asset['name']: asset['browser_download_url']
                      for asset in assets}

        # Return name Clash.for.Windows.Setup.x.xx.x.exe
        # Check all names contains Setup
        for name in asset_urls:
            if 'win.7z' in name and 'ia32' not in name and 'arm64' not in name:
                installer = name

        # Return url
        installer_url = asset_urls[installer]

        # ghproxy
        installer_url = ghproxy + installer_url

        return installer_url
    except:
        return ""


def cfa():
    try:
        # Get latest release
        r = requests.get(
            'https://api.github.com/repos/Kr328/ClashForAndroid/releases/latest', timeout=1)
        r.raise_for_status()
        release = r.json()

        # Get assets
        assets = release['assets']

        # Get name: url
        asset_urls = {asset['name']: asset['browser_download_url']
                      for asset in assets}

        # Return name Clash.for.Windows.Setup.x.xx.x.exe
        # Check all names contains Setup
        for name in asset_urls:
            if 'premium-universal-release' in name:
                installer = name

        # Return url
        installer_url = asset_urls[installer]

        # ghproxy
        installer_url = ghproxy + installer_url

        return installer_url
    except:
        return ""


def cfx():
    # Mac
    try:
        # Get latest release
        r = requests.get(
            'https://api.github.com/repos/yichengchen/clashX/releases/latest', timeout=1)
        r.raise_for_status()
        release = r.json()

        # Get assets
        assets = release['assets']

        # Get name: url
        asset_urls = {asset['name']: asset['browser_download_url']
                      for asset in assets}

        # Return name Clash.for.Windows.Setup.x.xx.x.exe
        # Check all names contains Setup
        for name in asset_urls:
            if '.dmg' in name:
                installer = name

        # Return url
        installer_url = asset_urls[installer]

        # ghproxy
        installer_url = ghproxy + installer_url

        return installer_url
    except:
        return ""


def ios():
    return "https://apps.apple.com/us/app/shadowrocket/id932747118"


def subscribe():
    # https://github.com/paimonhub/Paimonnode
    # https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml
    subscribe_source_name = "所有分享节点和订阅的组织和个人，由API自动聚合（来源见项目源码）"
    subscribe_source_url = "https://api.lwd-temp.top/api/dir/var/task/myutils/clash.py/"
    subscribe_url = "https://api.lwd-temp.top/api/clash/config" + \
        "?key=" + license.generate_key()
    base64_url = "https://api.lwd-temp.top/api/clash/base64" + \
        "?key=" + license.generate_key()

    # ghproxy
    # subscribe_url = ghproxy + subscribe_url
    # base64_url = ghproxy + base64_url

    return subscribe_source_name, subscribe_source_url, subscribe_url, base64_url


def render(china=False):
    subscribe_source_name, subscribe_source_url, subscribe_url, base64_url = subscribe()

    chinaclass = "notchina"
    # URL Encoded
    subscribe_encoded_url = urllib.parse.quote(subscribe_url, safe='')

    if china:
        chinaclass = "china"
    else:
        chinaclass = "notchina"

    dateStr = datetime.datetime.now(tz=pytz.timezone(
        'Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")

    return flask.render_template('clash.html', cfw=cfw(), cfw_portable=cfw_portable(), cfa=cfa(), subscribe_source_name=subscribe_source_name, subscribe_source_url=subscribe_source_url, subscribe_url=subscribe_url, base64_url=base64_url, subscribe_encoded_url=subscribe_encoded_url, china=chinaclass, date=dateStr, mac=cfx(), ip=cfstyle.get_ip())


def config(base64=False):
    # Get yaml and return

    # Start time
    start = time.time()

    sub_urls = [
        # "https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml",
        "https://sub.pmsub.me/clash.yaml",
        "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
        "https://raw.githubusercontent.com/openrunner/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/config.yaml",
        "https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/clash/config.yaml",
        "https://gitlab.com/free9999/ipupdate/-/raw/master/clash/config.yaml",
        "https://gitlab.com/free9999/ipupdate/-/raw/master/clash/2/config.yaml",
        "https://gitlab.com/free9999/ipupdate/-/raw/master/clash/3/config.yaml",
        "https://sub.sharecentre.online/sub",
        "https://sub.cloudflare.quest/"
        # "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml" # 长期不更新
        # "https://github.com/yu-steven/openit" # 纪念
    ]

    api_urls = [
        "https://sub.xeton.dev/sub",
        "https://api.wcc.best/sub",
        "https://api.dler.io/sub",
        "https://api.sublink.dev/sub",
        "https://sub.id9.cc/sub",
        "https://sub.maoxiongnet.com/sub"
    ]

    # Get an available API url
    api_url = False
    for url in api_urls:
        try:
            api = requests.get(url, timeout=1)
        except:
            continue

        if api.status_code == 400:
            api_url = url
            break

    if api_url:
        # try
        try:
            # API is available

            # Get sub list
            subs = []
            for url in sub_urls:
                try:
                    config = requests.get(url, timeout=1)
                except:
                    continue

                if config.status_code == 200:
                    subs.append(url)

            # API args
            # target=clash&new_name=true&url=
            # &insert=false&append_type=true&emoji=true&list=false&tfo=false&scv=false&fdn=true&sort=true

            # Pre-API-Args
            pre_api_args = "target=clash&new_name=true&url="

            if base64:
                pre_api_args = "target=v2ray&new_name=true&url="

            # Post-API-Args
            post_api_args = "&insert=false&append_type=true&emoji=true&list=false&tfo=false&scv=false&fdn=true&sort=true"

            api_call = api_url + "?"
            url_cmb = ""
            for sub in subs:
                url_cmb = url_cmb + "|"
                url_cmb = url_cmb + sub
            api_args = pre_api_args + \
                urllib.parse.quote(url_cmb, safe='') + post_api_args
            api_call = api_call + api_args
            api_req = requests.get(api_call, timeout=5)
            api_req.raise_for_status()
            config = api_req.text

            # End time
            end = time.time()
            delta = end - start

            debug_info = {"api_url": api_url,
                          "subs": subs, "api_call": api_call, "timestamp": time.time(), "duration": delta}
            config = "# " + json.dumps(debug_info) + " #" + "\n" + config
        except:
            # Same
            # No API available
            for url in sub_urls:
                import traceback
                trace = traceback.format_exc()

                allowed = ".yaml"

                if base64:
                    allowed = "sub"

                # Clash yaml only
                if url.endswith(allowed):
                    pass
                else:
                    continue

                try:
                    config = requests.get(url, timeout=1)
                except:
                    continue

                if config.status_code != 200:
                    continue
                else:
                    # config.raise_for_status()
                    config = config.text
                    debug_info = {"sub": url, "trace": trace,
                                  "error": "Error while calling API.", "timestamp": time.time()}
                    config = "# " + \
                        json.dumps(debug_info) + " #" + "\n" + config
                    break

    else:
        # No API available
        for url in sub_urls:

            allowed = ".yaml"

            if base64:
                allowed = "sub"

            # Clash yaml only
            if url.endswith(allowed):
                pass
            else:
                continue

            try:
                config = requests.get(url, timeout=1)
            except:
                continue

            if config.status_code != 200:
                continue
            else:
                # config.raise_for_status()
                config = config.text
                debug_info = {
                    "sub": url, "error": "No API available.", "timestamp": time.time()}
                config = "# " + json.dumps(debug_info) + " #" + "\n" + config
                break

    if base64:
        # Deleting the first 1 lines of a string(debug_info)
        # string.find('\n')会返回第一个换行符的位置，加1表示从第二行开始切片，最后将切片后的字符串保存到new_string变量中
        config = config[config.find('\n')+1:]

    return config

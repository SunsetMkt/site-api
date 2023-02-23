import flask
import requests
import urllib.parse

from . import keybase

ghproxy = keybase.ghproxy


def cfw():
    # Get latest release
    r = requests.get(
        'https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest')
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


def cfw_portable():
    # Get latest release
    r = requests.get(
        'https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest')
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


def cfa():
    # Get latest release
    r = requests.get(
        'https://api.github.com/repos/Kr328/ClashForAndroid/releases/latest')
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


def subscribe():
    # https://github.com/paimonhub/Paimonnode
    # https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml
    subscribe_source_name = "paimonhub/Paimonnode"
    subscribe_source_url = "https://github.com/paimonhub/Paimonnode"
    subscribe_url = "https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml"
    base64_url = "https://raw.githubusercontent.com/paimonhub/Paimonnode/main/base64"

    # ghproxy
    subscribe_url = ghproxy + subscribe_url
    base64_url = ghproxy + base64_url

    return subscribe_source_name, subscribe_source_url, subscribe_url, base64_url


def render():
    subscribe_source_name, subscribe_source_url, subscribe_url, base64_url = subscribe()

    # URL Encoded
    subscribe_encoded_url = urllib.parse.quote(subscribe_url)

    return flask.render_template('clash.html', cfw=cfw(), cfw_portable=cfw_portable(), cfa=cfa(), subscribe_source_name=subscribe_source_name, subscribe_source_url=subscribe_source_url, subscribe_url=subscribe_url, base64_url=base64_url, subscribe_encoded_url=subscribe_encoded_url)


def config():
    # Get yaml and return
    # https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml
    config_urls = [
        "https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml",
        "https://sub.pmsub.me/clash.yaml",
        "https://sub.xeton.dev/sub?target=clash&new_name=true&url=%7Chttps%3A%2F%2Fraw.githubusercontent.com%2FPawdroid%2FFree-servers%2Fmain%2Fsub%7Chttps%3A%2F%2Fraw.githubusercontent.com%2Fopenrunner%2Fclash-freenode%2Fmain%2Fclash.yaml%7Chttps%3A%2F%2Fraw.githubusercontent.com%2Flearnhard-cn%2Ffree_proxy_ss%2Fmain%2Fconfig.yaml&insert=false&append_type=true&emoji=true&list=false&tfo=false&scv=false&fdn=true&sort=true",
        "https://sub.xeton.dev/sub?target=clash&new_name=true&url=https%3A%2F%2Fraw.githubusercontent.com%2FPawdroid%2FFree-servers%2Fmain%2Fsub&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini",
        "https://raw.githubusercontent.com/openrunner/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/config.yaml"
    ]

    for url in config_urls:
        config = requests.get(url)
        if config.status_code != 200:
            continue
        else:
            config.raise_for_status()
            config = config.text
            break

    return config

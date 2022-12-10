import flask
import requests

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
    # https://github.com/ermaozi/get_subscribe
    # https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml
    subscribe_source_name = "ermaozi/get_subscribe"
    subscribe_source_url = "https://github.com/ermaozi/get_subscribe"
    subscribe_url = "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml"

    # ghproxy
    subscribe_url = ghproxy + subscribe_url

    return subscribe_source_name, subscribe_source_url, subscribe_url


def render():
    subscribe_source_name, subscribe_source_url, subscribe_url = subscribe()

    return flask.render_template('clash.html', cfw=cfw(), cfw_portable=cfw_portable(), cfa=cfa(), subscribe_source_name=subscribe_source_name, subscribe_source_url=subscribe_source_url, subscribe_url=subscribe_url)


def config():
    # Get yaml and return
    # https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml
    config = requests.get(
        "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml")
    config.raise_for_status()
    config = config.text

    return config

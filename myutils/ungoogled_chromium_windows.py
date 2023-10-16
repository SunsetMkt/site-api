# https://github.com/ungoogled-software/ungoogled-chromium-windows
import requests

from . import keybase

ghproxy = keybase.ghproxy


def get_latest_version():
    url = "https://api.github.com/repos/ungoogled-software/ungoogled-chromium-windows/releases/latest"
    r = requests.get(url)
    return r.json()["tag_name"]


def get_latest_download_url():
    # Get latest release of ungoogled-software/ungoogled-chromium-windows
    r = requests.get(
        "https://api.github.com/repos/ungoogled-software/ungoogled-chromium-windows/releases/latest"
    )
    r.raise_for_status()
    release = r.json()

    # Get assets
    assets = release["assets"]

    # Get name: url
    asset_urls = {asset["name"]: asset["browser_download_url"] for asset in assets}

    # Return name with installer and x64
    installer = [name for name in asset_urls if "installer" in name and "x64" in name][
        0
    ]

    # Return url
    installer_url = asset_urls[installer]

    # Get real url
    # r = requests.get(installer_url, allow_redirects=False)
    # r.raise_for_status()
    # installer_url = r.headers['Location']

    return ghproxy + installer_url

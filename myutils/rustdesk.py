# https://github.com/rustdesk/rustdesk
import requests

from . import keybase

ghproxy = keybase.ghproxy


def get_latest_release():
    url = 'https://api.github.com/repos/rustdesk/rustdesk/releases/latest'
    r = requests.get(url)
    return r.json()


def get_download_link(platform):
    # win32 win64 android
    # rustdesk-*-windows_x32.zip rustdesk-*-windows_x64.zip rustdesk-*.apk
    if platform == 'win32':
        platform = 'windows_x32.zip'
    elif platform == 'win64':
        platform = 'windows_x64.zip'
    elif platform == 'android':
        platform = '.apk'
    else:
        raise ValueError('Invalid platform')
    release = get_latest_release()
    assets = release['assets']
    asset_urls = {asset['name']: asset['browser_download_url']
                  for asset in assets}
    installer = [
        name for name in asset_urls if platform in name][0]
    installer_url = asset_urls[installer]
    return ghproxy + installer_url

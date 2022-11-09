# https://ftp.mozilla.org/pub/firefox/releases/latest/README.txt
import requests


def get_latest_firefox_version():
    url = 'https://product-details.mozilla.org/1.0/firefox_versions.json'
    r = requests.get(url)
    return r.json()['LATEST_FIREFOX_VERSION']


def win32():
    # https://download.mozilla.org/?product=firefox-latest&os=win&lang=zh-CN
    url = 'https://download.mozilla.org/?product=firefox-latest&os=win&lang=zh-CN'
    # Request and get redirect url
    r = requests.get(url, allow_redirects=False)
    return r.headers['Location']


def win64():
    # https://download.mozilla.org/?product=firefox-latest&os=win64&lang=zh-CN
    url = 'https://download.mozilla.org/?product=firefox-latest&os=win64&lang=zh-CN'
    # Request and get redirect url
    r = requests.get(url, allow_redirects=False)
    return r.headers['Location']


if __name__ == '__main__':
    print(get_latest_firefox_version())
    print(win32())
    print(win64())

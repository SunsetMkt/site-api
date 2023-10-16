# Get latest realease from huanghongxun/HMCL, get download url
import requests

from . import keybase

ghproxy = keybase.ghproxy


def get_latest_release(ext="exe"):
    # ext = 'exe' or 'jar' or 'sh'
    url = "https://api.github.com/repos/huanghongxun/HMCL/releases/latest"
    r = requests.get(url)
    if r.status_code == 200:
        for asset in r.json()["assets"]:
            if asset["name"].endswith(ext):
                return ghproxy + asset["browser_download_url"]
    return None


if __name__ == "__main__":
    print(get_latest_release("exe"))

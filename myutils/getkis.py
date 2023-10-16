# https://www.kaspersky.com.cn/downloads/internet-security-free-trial
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}


def getKis():
    response = requests.get(
        "https://api-router.kaspersky-labs.com/downloads/search/v3/b2c?productcodes=2910744&businesspurposes=Trial&sites=https%3A%2F%2Fwww.kaspersky.com.cn"
    )
    versions = response.json()[0]["response"]["Windows"]["KIS"]["Build"][
        "https://www.kaspersky.com.cn"
    ]
    for i in versions:
        # Get the largest version from key
        if i == max(versions.keys()):
            return versions[i]["zh-Hans-CN"]["Link"]


if __name__ == "__main__":
    print(getKis())

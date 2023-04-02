# https://v1.hitokoto.cn/
import requests

API_URL = "https://v1.hitokoto.cn/"


def main():
    htkt = requests.get(API_URL).json()
    return htkt

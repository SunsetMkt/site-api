import lxml.html
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def get_first_item_url():
    home = "https://news.cyol.com/gb/channels/vrGlAKDl/index.html"
    r = requests.get(home, headers=headers)
    r.encoding = 'utf-8'
    html = lxml.html.fromstring(r.text)
    # xpath
    url1 = html.xpath('/html/body/div[2]/div/ul/li[1]/a[1]/@href')[0]
    return url1


def get_title_and_icon(url):
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    html = lxml.html.fromstring(r.text)
    title = html.xpath('/html/head/title/text()')[0]
    icon_url = url.split('m.html')[0] + "images/icon.jpg"
    # fetch icon
    # r = requests.get(icon_url, headers=headers)
    # icon = base64.b64encode(r.content).decode()
    # base64 with mime type
    # icon = "data:image/jpeg;base64," + icon
    return title, icon_url, url


def get():
    url = get_first_item_url()
    title, icon, url = get_title_and_icon(url)
    return title, icon, url

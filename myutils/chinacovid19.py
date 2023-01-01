import flask
import lxml.html
import requests

list_page = "https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}


def get_latest_page_url():
    r = requests.get(list_page, headers=headers)
    r.raise_for_status()
    # Get class jal-item-list
    root = lxml.html.fromstring(r.text)
    # Get the first <a> tag
    a = root.xpath('//ul[@class="jal-item-list"]/li[1]/a')[0]
    href = a.get('href')
    # Combine href and list_page
    href = href.replace('./', list_page)
    return href


def pharse_detail_page(url):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    root = lxml.html.fromstring(r.text)
    # Get title
    p = root.xpath('//p[@class="cn-main-title"]')[0]
    title = p.text_content()
    # Get content, div cn-main-detail
    div = root.xpath('//div[@class="cn-main-detail"]')[0]
    # Remove style and script
    for e in div.xpath('//style | //script'):
        e.getparent().remove(e)
    # Get any text in it
    ps = div.xpath('.//text()')
    content = '\n'.join(ps).strip()
    return title, content


def render_page():
    page = get_latest_page_url()
    title, content = pharse_detail_page(page)
    return flask.render_template("gist.html", title=title, gist=content)

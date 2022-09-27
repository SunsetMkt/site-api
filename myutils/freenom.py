# https://raw.githubusercontent.com/SunYufei/freenom/master/run.py
import re

import requests


def fnRenew(username, password):
    log = ''

    # 登录地址
    LOGIN_URL = 'https://my.freenom.com/dologin.php'
    # 域名状态地址
    DOMAIN_STATUS_URL = 'https://my.freenom.com/domains.php?a=renewals'
    # 域名续期地址
    RENEW_DOMAIN_URL = 'https://my.freenom.com/domains.php?submitrenewals=true'

    # token 正则
    token_ptn = re.compile('name="token" value="(.*?)"', re.I)
    # 域名信息正则
    domain_info_ptn = re.compile(
        r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>',
        re.I)
    # 登录状态正则
    login_status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)

    # request session
    sess = requests.Session()
    sess.headers.update({
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/103.0.5060.134 Safari/537.36'
    })

    # login
    sess.headers.update({
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'https://my.freenom.com/clientarea.php'
    })
    r = sess.post(LOGIN_URL, data={'username': username, 'password': password})
    if r.status_code != 200:
        return 'login failed'

    # check domain status
    sess.headers.update({'referer': 'https://my.freenom.com/clientarea.php'})
    r = sess.get(DOMAIN_STATUS_URL)

    # login status check
    if not re.search(login_status_ptn, r.text):
        return 'get login status failed'

    # page token
    match = re.search(token_ptn, r.text)
    if not match:
        return 'get page token failed'

    token = match.group(1)

    # domains
    domains = re.findall(domain_info_ptn, r.text)

    # renew domains
    for domain, days, renewal_id in domains:
        days = int(days)
        if days < 14:
            sess.headers.update({
                'referer':
                f'https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}',
                'content-type': 'application/x-www-form-urlencoded'
            })
            r = sess.post(RENEW_DOMAIN_URL,
                          data={
                              'token': token,
                              'renewalid': renewal_id,
                              f'renewalperiod[{renewal_id}]': '12M',
                              'paymentmethod': 'credit'
                          })
            if r.text.find('Order Confirmation') != -1:
                log += domain + '续期成功' + '\n'
            else:
                log += domain + '续期失败' + '\n'
        log += f'{domain} 还有 {days} 天续期' + '\n'

    return log

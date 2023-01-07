import datetime

import flask
import requests

from . import keybase

username = keybase.username

yellow_alert_days = 14
red_alert_days = 28


def get_github_last_activity_time(name):
    url = 'https://api.github.com/users/' + name
    r = requests.get(url)
    r.raise_for_status()
    updatedat = r.json()['updated_at']
    return datetime.datetime.strptime(updatedat, '%Y-%m-%dT%H:%M:%SZ')


def get_days_since(time):
    return (datetime.datetime.now() - time).days


def get_alive_info(name):
    try:
        time = get_github_last_activity_time(name)
    except:
        return 'error', 'error', 'error'
    days = get_days_since(time)
    if days > red_alert_days:
        return 'red', days, time
    elif days > yellow_alert_days:
        return 'yellow', days, time
    else:
        return 'green', days, time


def time_to_str(time):
    # Return a string like '2018-01-01 00:00:00 UTC'
    return time.strftime('%Y-%m-%d %H:%M:%S UTC')


def render():
    name = username
    color, days, time = get_alive_info(name)
    if color == 'error':
        title = '无法获取活跃信息'
        subtitle = f'无法获取 {name} 的活跃信息'
        message = ''
    elif color == 'green':
        title = '一切正常'
        subtitle = f'{name} 在 {time_to_str(time)} 在 GitHub 上有活动，至今 {days} 天'
        message = '这是一个演示目的的页面，警报无实际意义。'
    elif color == 'yellow':
        title = '黄色警报'
        subtitle = f'{name} 在 {time_to_str(time)} 在 GitHub 上有活动，至今 {days} 天'
        message = '这是一个演示目的的页面，警报无实际意义。'
    elif color == 'red':
        title = '红色警报'
        subtitle = f'{name} 在 {time_to_str(time)} 在 GitHub 上有活动，至今 {days} 天'
        message = '这是一个演示目的的页面，警报无实际意义。'
    else:
        raise ValueError('Unknown color')
    return flask.render_template('alive.html', title=title, subtitle=subtitle, message=message, color=color)

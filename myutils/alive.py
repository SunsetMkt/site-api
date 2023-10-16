import datetime

import flask
import requests

from . import keybase

username = keybase.username

yellow_alert_days = 14
red_alert_days = 28


def get_github_last_activity_time(name):
    # https://stackoverflow.com/a/37554614/20675299
    url = "https://api.github.com/users/" + name + "/events"
    r = requests.get(url)
    r.raise_for_status()
    # get latest event time
    try:
        latest = r.json()[0]["created_at"]
    except IndexError:
        # 时间表中只包含过去 90 天内创建的事件。 超过 90 天的活动将不包括在内（即使时间表中的活动总数不到 300 个）。
        latest = "1970-01-01T00:00:00Z"

    return datetime.datetime.strptime(latest, "%Y-%m-%dT%H:%M:%SZ"), r.text


def get_days_since(time):
    return (datetime.datetime.now() - time).days


def get_alive_info(name):
    try:
        time, code = get_github_last_activity_time(name)
    except:
        return "error", "error", "error", "error"
    days = get_days_since(time)
    if days > 90:
        return "timeout", days, time, code
    if days > red_alert_days:
        return "red", days, time, code
    elif days > yellow_alert_days:
        return "yellow", days, time, code
    else:
        return "green", days, time, code


def time_to_str(time):
    # Return a string like '2018-01-01 00:00:00 UTC'
    return time.strftime("%Y-%m-%d %H:%M:%S UTC")


def render():
    name = username
    color, days, time, code = get_alive_info(name)
    if color == "error":
        title = "无法获取活跃信息"
        subtitle = f"无法获取 {name} 的活跃信息"
        message = ""
    elif color == "timeout":
        color = "red"
        title = "红色警报"
        subtitle = f"{name} 在 GitHub 上无活动超过90天"
        message = f"最后活跃时间未知，因为 GitHub API 仅提供最近90天的活动。这是一个演示目的的页面，警报无实际意义。"
    elif color == "green":
        title = "一切正常"
        subtitle = f"{name} 在 {time_to_str(time)} 在 GitHub 上有活动，至今 {days} 天"
        message = "这是一个演示目的的页面，警报无实际意义。"
    elif color == "yellow":
        title = "黄色警报"
        subtitle = f"{name} 在 {time_to_str(time)} 在 GitHub 上有活动，至今 {days} 天"
        message = "这是一个演示目的的页面，警报无实际意义。"
    elif color == "red":
        title = "红色警报"
        subtitle = f"{name} 在 {time_to_str(time)} 在 GitHub 上有活动，至今 {days} 天"
        message = "这是一个演示目的的页面，警报无实际意义。"
    else:
        raise ValueError("Unknown color")
    return flask.render_template(
        "alive.html",
        title=title,
        subtitle=subtitle,
        message=message,
        color=color,
        code=code,
    )

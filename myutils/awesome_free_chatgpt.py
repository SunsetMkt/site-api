import flask
import requests


def getREADME():
    # https://github.com/LiLittleCat/awesome-free-chatgpt
    url = "https://raw.githubusercontent.com/LiLittleCat/awesome-free-chatgpt/main/README.md"
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def readmeParser(text):
    available = []
    whiteWords = ["🆓"]
    blackWords = ["🔐", "🌎"]
    for line in text.split("\n"):
        # Must have whiteWords & should not have blackWords
        if any(word in line for word in whiteWords) and not any(
            word in line for word in blackWords
        ):
            available.append(line)
    return available


def main():
    # available = readmeParser(getREADME())
    # markdown = "\n".join(available)
    markdown_content = getREADME()
    return flask.render_template(
        "gist.html", title="awesome-free-chatgpt", gist=markdown_content
    )

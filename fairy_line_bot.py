# -*- coding: utf-8 -*-

import os
from flask import Flask, request
import requests
import json

app = Flask(__name__)

REPRY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
FAIRY_STRING = '妖精'
schedule = "予定"
register = "登録"

LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID': os.environ['ChannelID'],
    'X-Line-ChannelSecret': os.environ['ChannelSecret'],
    'X-Line-Trusted-User-With-ACL': os.environ['MID']
}


def generate_text(text):
    content = ""
    if FAIRY_STRING in text:
        if schedule in text and register in text:
            # 予定を登録
            content = "登録フォーム\n https://goo.gl/forms/fjoodUy89O0BFFqv1"
            c
        else:
            content = "呼んだ？"
    else:
        content = text
    return content


def postMessage(replyToken, text):
    textResponse = [{'type': 'text', 'text': text}]
    reply = {'replyToken': replyToken, 'messages': textResponse}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + LINE_HEADERS['X-Line-Trusted-User-With-ACL']
    }
    r = requests.post(REPRY_ENDPOINT, data=json.dumps(reply), headers=headers)
    print(r.text)


@app.route('/webhook', methods=['POST'])
def webhook():
    events = request.json["events"]
    for event in events:
        replyToken = event["replyToken"]

        if event['message']['type'] == 'text':
            text = event['message']['text']
            content = generate_text(text)
            postMessage(replyToken, content)

    return ''


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

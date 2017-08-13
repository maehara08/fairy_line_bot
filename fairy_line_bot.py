import os
from flask import Flask, request
import requests

app = Flask(__name__)

REPRY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID': os.environ['ChannelID'],
    'X-Line-ChannelSecret': os.environ['ChannelSecret'],
    'X-Line-Trusted-User-With-ACL': os.environ['MID']
}


def postMessage(replyToken, text):
    textResponse = {'type': 'text', 'text': text}
    reply = {'replyToken': replyToken, 'messages': textResponse}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(LINE_HEADERS['X-Line-Trusted-User-With-ACL'])
    }
    requests.post(REPRY_ENDPOINT, headers=headers, data=reply)


@app.route('/webhook', methods=['POST'])
def webhook():
    events = request.json["events"]
    for event in events:
        print("events")
        print(events)
        replyToken = event["replyToken"]
        print("replytoken")
        print(replyToken)

        if event['message']['type'] == 'text':
            text = event['message']['type']['text']
            postMessage(replyToken, text)

    return ''


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

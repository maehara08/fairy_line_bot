# -*- coding: utf-8 -*-

import os
from flask import Flask, request
import requests
import redis
import json

app = Flask(__name__)

docomoApiKey = os.environ['DOCOMO_API_KEY']
REDIS_URL = os.environ['REDIS_URL']
RedisKey = "context_key"

REPRY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
docomo_endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
docomo_url = docomo_endpoint.replace('REGISTER_KEY', docomoApiKey)

FAIRY_STRING = '妖精'
schedule = "予定"
register = "登録"
tano = "たの"

LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID': os.environ['ChannelID'],
    'X-Line-ChannelSecret': os.environ['ChannelSecret'],
    'X-Line-Trusted-User-With-ACL': os.environ['MID']
}

# データベースの指定
DATABASE_INDEX = 1  # 0じゃなくあえて1
# コネクションプールから１つ取得
pool = redis.ConnectionPool.from_url(REDIS_URL, db=DATABASE_INDEX)
# コネクションを利用
redisConnection = redis.StrictRedis(connection_pool=pool)


def generate_text(text):
    content = ""
    if FAIRY_STRING in text:
        if schedule in text and register in text:
            # 予定を登録
            content = "登録フォーム\n https://goo.gl/forms/fjoodUy89O0BFFqv1"
        else:
            content = "呼んだ？"
    elif tano in text:
        content = "かわいい"
    else:
        payload = {'utt': text, 'context': redisConnection.get(RedisKey)}
        headers = {'Content-type': 'application/json'}

        r = requests.post(docomo_url, data=json.dumps(payload), headers=headers)
        data = r.json()
        content = data['utt']
        context = data['context']
        redisConnection.set(RedisKey, context)
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

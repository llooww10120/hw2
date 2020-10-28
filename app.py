# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import random #added
import json #added
from flask import jsonify #added

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', '0')
#channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '0')
#channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    #sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    #sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

#HW1方法
def count(n1, n2, operator):
    if operator == '+':
        return n1 + n2
    elif operator == '-':
        return n1 - n2
    elif operator == '%':
        return (n1 % n2)
    elif operator == '*':
        return n1 * n2
    

@app.route("/hw2", methods= ['POST', 'GET'])
def hw2():
    body = request.get_data(as_text= True)
    
    print(body)
    jBody = json.loads(body)
    question = jBody['Question']
    print(question)    

    userId = 'ntustb10730026'
    if question.find('|') != -1:    
        answer = "".join(question.split(' '))
        answer = answer.replace('|',userId)
    else:
        question = question.split(' ')
        answer = count(int(question[0]), int(question[2]), question[1])
    
    tempDict = {}
    tempDict['Result'] = answer
    return jsonify(tempDict)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        if event.message.text == "擲骰子":
            dice = random.randint(1, 6)
            theMessage = f'您擲到 {dice} 點'
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=theMessage)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug') #原本default=False
    options = arg_parser.parse_args()

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=options.debug, port=port, host='0.0.0.0')

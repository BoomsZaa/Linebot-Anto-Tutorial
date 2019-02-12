from flask import Flask, request
import antolib
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi('wYMUKxKUEd8UU3ZknVLJXzxslvKee+sgac4r9NwO0soFPwtxbgC19ddumUbV2eo4mejaN+gQZSfuPfEsMgV5+7TuQTzJxdFg0qMc5NCg6EUYjZL4guGO0qeHn3gnAL9IMUbTP1tsYCDKnP7jxeXBzwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6097be547eea8294db40c7dbb6a4a566')

app = Flask(__name__)

# username of anto.io account
user = 'BoomsKunG'
# key of permission, generated on control panel anto.io
key = 'ObbVFdRsiP5QOcjCk4qcZtqHvH1h3kfWFh0CJIF4'
# your default thing.
thing = 'myDevice'

anto = antolib.Anto(user, key, thing)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if(message == 'channel1 on'):
        anto.pub('myChannel1', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On channel1"))
    elif(message == 'channel1 off'):
        anto.pub('myChannel1', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel1"))
    elif(message == 'channel2 on'):
        anto.pub('myChannel2', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On channel2"))
    elif(message == 'channel2 off'):
        anto.pub('myChannel2', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel2"))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="Turn Off channel1"))

if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)

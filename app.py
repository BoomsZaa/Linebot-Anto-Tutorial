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
key = 'Oo1Aeoi3Y2Jy5HYG4QLcft0tNz6PTCObBu3d6qSO'
# your default thing.
thing = 'catbot'

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
	if(message == 'on'):
        anto.pub('ch1', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On"))
    elif(message == 'off'):
        anto.pub('ch1', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off"))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="Turn Off channel1"))

if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)

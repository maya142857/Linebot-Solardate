from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# Channel Secret
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
import datetime
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_str = event.message.text
    if len(input_str) == 8:
        message = TextSendMessage(text=date_to_solar(input_str))
    elif len(input_str) == 4:
        message = TextSendMessage(text=solar_to_date(input_str))
    else:
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg',
                title='Solardate Calculator',
                text='Hope it helps...',
                actions=[
                    MessageTemplateAction(
                        label='使用教學',
                        text='輸入4碼數字：太陽日→年月日\n輸入8碼數字：年月日→太陽日'
                    ),
                    URITemplateAction(
                        label='問題回報',
                        uri='https://github.com/maya142857/Linebot-Solardate/issues'
                    )
                ]
            )
        )
    line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

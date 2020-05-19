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

def date_to_solar(input_str):
    y = int(input_str[0:4])
    m = int(input_str[4:6])
    d = int(input_str[6:8])
  
    sday = datetime.date(y, m, d)
    count = sday - datetime.date(sday.year - 1, 12 ,31) # minus the last day in last yeae
  
    return ('%s%03d' % (str(y)[3:4],count.days))

def solar_to_date(input_str):
    output_num = 2
    y = int(input_str[0:1])
    d = int(input_str[1:4])
    temp = datetime.datetime.now().year
    year_list = []
    date_list = []
    while len(year_list) < output_num:
        if y == temp%10:
            year_list.append(temp)
            temp = temp - 1
        else:
            temp = temp - 1
    for year in year_list:
        date = datetime.date(year-1,12,31) + datetime.timedelta(days=d)
        date = date.strftime('%Y-%m-%d')
        date_list.append(date)

    print_data = date_list[0] + ', ' + date_list[1]
    return (print_data)

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


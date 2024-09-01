'''
-*- coding: utf-8 -*-

Reference: https://github.com/line/line-bot-sdk-python/tree/master

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
Google Cloud Run functions usage
Runtime: Python >= 3.8, usually 3.12
Entry point: callback
'''

import functions_framework
from flask import Flask, request, abort
import extend_url
import os
import json

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), 'line_channel_details.json')) as f:
    line_channel_details = json.load(f)

    channel_access_token = line_channel_details['channel_access_token']
    channel_secret = line_channel_details['channel_secret']

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

@functions_framework.http
@app.route("/callback", methods=['POST'])
def callback(request):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@functions_framework.http
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # user_input = event.message.text

    bucket_name = 'tir102_apod'
    blob_name = '2024-08-25.jpg'
    credentials = extend_url.credentials

    image_url = extend_url.generate_signed_url(bucket_name, blob_name, credentials)

    # video_url = 'https://www.youtube.com/watch?v=CwrvN0Q9_Sg'

    # constellations = [
    #     '牡羊座',
    #     '金牛座',
    #     '雙子座',
    #     '巨蟹座',
    #     '獅子座',
    #     '處女座',
    #     '天秤座',
    #     '天蠍座',
    #     '射手座',
    #     '摩羯座',
    #     '水瓶座',
    #     '雙魚座',
    # ]

    # text_message = TextMessage(text=user_input)
    # text_message = TextMessage(text=image_url)
    # text_message = TextMessage(text=video_url)

    image_message = ImageMessage(
        original_content_url=image_url,
        preview_image_url=image_url,
    )

    # constellation_buttons = TextMessage(
    #     text='星座',
    #     quick_reply=QuickReply(
    #         items=[
    #             QuickReplyItem(
    #                 action=MessageAction(
    #                     label=c,
    #                     text=c,
    #                 )
    #             )
    #             for c in constellations
    #         ]
    #     )
    # )

    messages = [
        # text_message,
        image_message,
        # constellation_buttons,
    ]
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages,
            )
        )

if __name__ == "__main__":
    app.run()

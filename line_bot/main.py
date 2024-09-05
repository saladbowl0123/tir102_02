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
import check_date
import extend_url
import select_from_bigquery
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

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    INVALID_DATE = '日期無效 Invalid date'
    DATE_USAGE = '日期用法 Date usage: `yyyy-mm-dd`'
    DATE_OUT_OF_RANGE = '以前無資料 No data before'
    NO_DATA_TODAY = '尚未獲得今日資料 Data not yet available for today'
    NO_DATA_AT_DATE = '無資料 No data at'

    APOD_COLUMN_NAMES_OUTPUT_ORDER = [
        'date',
        'title',
        'explanation',
        'copyright',
    ]

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

    user_input = event.message.text
    user_input = user_input.strip()
    user_input = user_input.lower()

    messages = []

    date = check_date.check_date(user_input)

    if not date:
        text_message = '\n'.join([INVALID_DATE, DATE_USAGE])
    elif not check_date.is_in_range(date):
        text_message = f'{check_date.OLDEST} {DATE_OUT_OF_RANGE} {check_date.OLDEST}'
    else:
        # date is valid and in range
        apod = select_from_bigquery.query_apod(date)

        if apod.empty:
            if date == check_date.today():
                text_message = NO_DATA_TODAY
            else:
                # some dates have no data
                text_message = f'{date} {NO_DATA_AT_DATE} {date}'
        else:
            # data found
            text_message = []

            for column in APOD_COLUMN_NAMES_OUTPUT_ORDER:
                reformatted_column_name = reformat_column_name(column)
                value = apod.loc[0][column]
                text_message_new_line = f'{reformatted_column_name}: {value}'
                text_message.append(text_message_new_line)

            text_message = '\n'.join(text_message)

            match apod.loc[0]['media_type']:
                case 'image':
                    image_message = reformatted_date_str_to_image_message(reformatted_date_str)
                    messages.append(image_message)
                case 'video':
                    # videos cannot normally be directly downloaded from YouTube
                    # but LINE automatically embeds YouTube videos by URL in text messages
                    video_url = apod.loc[0]['URL']
                    text_message = f'{text_message}\n{video_url}'

    text_message = TextMessage(text=text_message)
    messages.append(text_message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages,
            )
        )

def reformat_column_name(column):
    return (' '.join(column.split('_'))
        .lower()
        .capitalize()
    )

def date_to_image_message(date):
    # images from GCS database are named by `yyyy-mm-dd` date format
    bucket_name = 'tir102_apod'
    blob_name = f'{date}.jpg'
    credentials = extend_url.credentials

    image_url = extend_url.generate_signed_url(
        bucket_name,
        blob_name,
        credentials,
    )

    image_message = ImageMessage(
        original_content_url=image_url,
        preview_image_url=image_url,
    )

    return image_message

if __name__ == "__main__":
    app.run()

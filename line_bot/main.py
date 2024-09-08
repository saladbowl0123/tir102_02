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
import detect_language
import check_date
import extend_url
import select_from_bigquery
import os
import json
import random

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
    FollowEvent,
    MessageEvent,
    TextMessageContent,
)

HELLO = '感謝加入好友! Thanks for adding as a friend!'
BUTTONS_USAGE = '點選按鍵了解更多資訊 Tap a button to learn more\n向右滑動以查看更多按鍵 Scroll right for more buttons'
DATE_OUT_OF_RANGE = '以前無資料 No data before'
LANGUAGE_NOT_SUPPORTED = '不支援此語言 Language not supported'
NO_DATA = '無資料 No data'
NO_DATA_TODAY = '尚未獲得今日資料 Data not yet available for today'
NO_DATA_AT_DATE = '無資料 No data at'

USAGE_COMMANDS = [
    '用法',
    '說明',
    'usage',
    'manual',
    'help',
]

USAGE_LABELS = [
    'planet',
    'constellation',
    'satellite',
    'comet',
    'shower',
    'sun',
]

APOD_COLUMN_NAMES_OUTPUT_ORDER = [
    'date',
    'title',
    'copyright',
]

USAGE = '\n'.join(
    [
        '使用下列指令重新產生此訊息 regenerate this message with the following commands:',
        ', '.join(f"'{command}'" for command in USAGE_COMMANDS),
        '用法 Usage:',
        '- 中文關鍵詞',
        '- English keyword',
        '- 日期用法 Date usage: `yyyy-mm-dd`',
        BUTTONS_USAGE,
    ]
)

with open(os.path.join(os.path.dirname(__file__), 'chinese_to_english.json')) as f:
    chinese_to_english = json.load(f)

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

@handler.add(FollowEvent)
def handle_follow(event):
    text = f'{HELLO}\n{USAGE}'
    labels = USAGE_LABELS
    text_message = text_to_text_message(text, labels)
    messages = [text_message]

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages,
            )
        )

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    process_date = False
    search_celestial_bodies = False
    random_date = False
    english_tag_to_dates = False

    user_input = event.message.text
    user_input = user_input.strip()
    user_input = user_input.lower()

    dates = []
    text_list = []
    messages = []

    image_message = None
    labels = None

    if user_input in USAGE_COMMANDS:
        text_list.append(USAGE)
        labels = USAGE_LABELS
    else:
        date = check_date.check_date(user_input)

        if date:
            if check_date.is_in_range(date):
                process_date = True
            else:
                text_list.append(f'{check_date.OLDEST} {DATE_OUT_OF_RANGE} {check_date.OLDEST}')
        elif detect_language.chinese_like(user_input):
            if user_input in chinese_to_english:
                user_input = chinese_to_english[user_input]
                search_celestial_bodies = True
            else:
                dates = select_from_bigquery.query_chinese_tag(user_input)
                random_date = bool(dates)
                if not random_date:
                    text_list.append(NO_DATA)
        elif detect_language.english_like(user_input):
            search_celestial_bodies = True
        elif detect_language.other_like(user_input):
            text_list.append(LANGUAGE_NOT_SUPPORTED)

        if search_celestial_bodies:
            if user_input in ['planet', 'planets']:
                text_list.append(BUTTONS_USAGE)
                planet_names = select_from_bigquery.query_planet_names()
                labels = [planet.title() for planet in planet_names]
            elif user_input in ['constellation', 'constellations']:
                text_list.append(BUTTONS_USAGE)
                constellation_names = select_from_bigquery.query_constellation_names()
                labels = [constellation.title() for constellation in constellation_names]
            else:
                english_tag_to_dates = True
                if user_input in ['satellite', 'satellites']:
                    satellite = select_from_bigquery.query_random_satellite()
                    df_text = df_to_text(satellite)
                    text_list.append(df_text)
                    user_input = satellite.loc[0]['Name']
                elif user_input in ['comet', 'comets']:
                    comet = select_from_bigquery.query_random_comet()
                    df_text = df_to_text(comet)
                    text_list.append(df_text)
                    user_input = comet.loc[0]['NAME']
                elif user_input in ['shower', 'showers']:
                    shower = select_from_bigquery.query_random_shower()
                    df_text = df_to_text(shower)
                    text_list.append(df_text)
                    user_input = shower.loc[0]['Shower']
                elif user_input in [planet_name.lower() for planet_name in select_from_bigquery.query_planet_names()]:
                    planet = select_from_bigquery.query_planet(user_input)
                    df_text = df_to_text(planet)
                    text_list.append(df_text)
                elif user_input in [constellation_name.lower() for constellation_name in select_from_bigquery.query_constellation_names()]:
                    constellation = select_from_bigquery.query_constellation(user_input)
                    df_text = df_to_text(constellation)
                    text_list.append(df_text)
                elif user_input in [satellite_name.lower() for satellite_name in select_from_bigquery.query_satellite_names()]:
                    satellite = select_from_bigquery.query_satellite(user_input)
                    df_text = df_to_text(satellite)
                    text_list.append(df_text)
                elif user_input in [comet_name.lower() for comet_name in select_from_bigquery.query_comet_names()]:
                    comet = select_from_bigquery.query_comet(user_input)
                    df_text = df_to_text(comet)
                    text_list.append(df_text)
                elif user_input in [shower_name.lower() for shower_name in select_from_bigquery.query_shower_names()]:
                    shower = select_from_bigquery.query_shower(user_input)
                    df_text = df_to_text(shower)
                    text_list.append(df_text)
                elif user_input == 'sun':
                    sun = select_from_bigquery.query_sun()
                    df_text = df_to_text(sun)
                    text_list.append(df_text)

            if english_tag_to_dates:
                dates = select_from_bigquery.query_english_tag(user_input)
                random_date = bool(dates)
                if not random_date:
                    text_list.append(NO_DATA)

        if random_date:
            # get random image or video corresponding to tag if possible
            date = random.choice(dates)
            process_date = True

        if process_date:
            apod = select_from_bigquery.query_apod(date)

            if apod.empty:
                if date == check_date.today():
                    text_list.append(NO_DATA_TODAY)
                else:
                    # some dates have no data
                    text_list.append(f'{date} {NO_DATA_AT_DATE} {date}')
            else:
                # APoD data found; parse it as text
                for column in APOD_COLUMN_NAMES_OUTPUT_ORDER:
                    reformatted_column_name = reformat_column_name(column)
                    value = apod.loc[0][column]
                    new_line = f'{reformatted_column_name}: {value}'
                    text_list.append(new_line)

                match apod.loc[0]['media_type']:
                    case 'image':
                        image_message = date_to_image_message(date)
                    case 'video':
                        # only images are stored in GCS and not videos
                        # because videos cannot normally be directly downloaded from YouTube
                        # but LINE automatically embeds YouTube videos by URL in text messages
                        video_url = apod.loc[0]['URL']
                        text_list.append(video_url)

    text = '\n'.join(text_list)
    text_message = text_to_text_message(text, labels)
    messages.append(text_message)

    if image_message:
        messages.append(image_message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages,
            )
        )

def text_to_text_message(text, labels=None):
    if labels:
        text_message = TextMessage(
            text=text,
            # construct buttons
            quick_reply=QuickReply(
                items=[
                    QuickReplyItem(
                        action=MessageAction(
                            label=label,
                            text=label,
                        )
                    )
                    for label in labels
                ]
            )
        )
    else:
        text_message = TextMessage(text=text)

    return text_message

def reformat_column_name(column):
    return (' '.join(column.split('_'))
        .lower()
        .capitalize()
    )

def df_to_text(df, output_order=None):
    text_list = []

    if not output_order:
        output_order = df.columns

    for column in output_order:
        reformatted_column_name = reformat_column_name(column)
        value = df.loc[0][column]
        if column in ['Start_date', 'End_date']:
            # show only `mm-dd` from constellation date period
            value = value.strftime('%m-%d')
        new_line = f'{reformatted_column_name}: {value}'
        text_list.append(new_line)

    text = '\n'.join(text_list)

    return text

def reformat_describe_df(df):
    index = df.index
    columns = df.columns

    index = dict(zip(index, [reformat_column_name(i) for i in index]))
    columns = dict(zip(columns, [reformat_column_name(c) for c in columns]))

    df = df.rename(
        index=index,
        columns=columns,
    )

    df_text = df.to_string()

    return df_text

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
